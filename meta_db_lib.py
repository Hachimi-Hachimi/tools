class MetaDb:
    def __init__(self, conn):
        self.cur = conn.cursor()

        res = self.cur.execute("SELECT n FROM c WHERE n = '//Android' OR n = '//Windows'")
        self.platform = res.fetchone()[0][2:]

    def get_asset_hash(self, name):
        res = self.cur.execute("SELECT h FROM a WHERE n = '{}'".format(name))
        return (res.fetchone() or (None,))[0]

    URL_FORMAT = "https://prd-storage-game-umamusume.akamaized.net/dl/resources/{}/assetbundles/{}/{}"
    def get_asset_bundle_url(self, asset_hash):
        return self.URL_FORMAT.format(self.platform, asset_hash[0:2], asset_hash)

    def get_asset_bundle_url_from_name(self, name):
        asset_hash = self.get_asset_hash(name)
        if not asset_hash:
            return None

        return self.get_asset_bundle_url(asset_hash)

    def find_flash_prefab(self, base_name):
        return self.cur.execute("SELECT n, h FROM a WHERE n LIKE 'uianimation/flash/%/pf_fl_{}'".format(base_name)).fetchone() # (name, hash)

    def find_flash_source_resources(self, base_name):
        return self.cur.execute("SELECT n, h FROM a WHERE n LIKE 'sourceresources/flash/%/fl_{0}/meshparameter/as_umeshparam_fl_{0}'".format(base_name)).fetchone() # (name, hash)