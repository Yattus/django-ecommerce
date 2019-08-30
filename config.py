# store/config.py
from oscar.config import Shop

class store(Shop):

    # Override the get_urls method to remove the URL configuration for the
    # dashboard app
    def get_urls(self):
        urls = super().get_urls()
        for urlpattern in urls[:]:
            if hasattr(urlpattern, 'app_name') and (urlpattern.app_name == 'checkout'):
                urls.remove(urlpattern)
        return self.post_process_urls(urls)
