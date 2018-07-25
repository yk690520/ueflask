#修正url
def fixUrl(url):
    url=url.replace("//","/")
    url=url.replace("\\\\","/")
    url=url.replace("\\","/")
    return url

print(fixUrl("/static/tmps/image/20180724/1532421996314511428.jpg"))