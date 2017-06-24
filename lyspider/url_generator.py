class URLGenerator:
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
        self.template_url = "http://gny.ly.com/list?src={}&dest={}&prop=0"

    def generate_urls(self):
        src_dest = [(x, y) for x in self.src for y in self.dest]
        urls = []
        for element in src_dest:
            url = self.template_url.format(element[0], element[1])
            urls.append(url)
        return urls
