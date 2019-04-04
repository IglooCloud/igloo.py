
from aiodataloader import DataLoader


class CategorySeriesValueLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{categorySeriesValue(id:"%s"){%s}}' % (self._id, fields), keys=["categorySeriesValue"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching device{id} the result is in the device key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class CategorySeriesValue:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = CategorySeriesValueLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def timestamp(self):
        if self.client.asyncio:
            return self.loader.load("timestamp")
        else:
            return self.client.query('{categorySeriesValue(id:"%s"){timestamp}}' % self._id, keys=[
                "categorySeriesValue", "timestamp"])

    @timestamp.setter
    def timestamp(self, newValue):
        self.client.mutation(
            'mutation{categorySeriesValue(id:"%s", timestamp:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def value(self):
        if self.client.asyncio:
            return self.loader.load("value")
        else:
            return self.client.query('{categorySeriesValue(id:"%s"){value}}' % self._id, keys=[
                "categorySeriesValue", "value"])

    @value.setter
    def value(self, newValue):
        self.client.mutation(
            'mutation{categorySeriesValue(id:"%s", value:"%s"){id}}' % (self._id, newValue), asyncio=False)
