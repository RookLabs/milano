class IocBundleDownloader(object):
    bundle_hash = 'http://'

    def __init__(self, bundle_url):
        pass

    def hash_of_existing_bundle():
        return 1

    def hash_of_latest_hosted_bundle():
        return 1

    def download_latest_bundle():
        pass

    def verify_bundle():
        pass

    def extract_bundle_contents():
        pass

    def conditionally_update_bundle_and_contents():
        local_hash = hash_of_existing_bundle()
        remote_hash = hash_of_latest_hosted_bundle()

        if local_hash != remote_hash:
            download_latest_bundle()

        verify_bundle()
        extract_bundle_contents()
