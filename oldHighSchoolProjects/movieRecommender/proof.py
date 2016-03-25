import urllib2

def proof(url):
    return urllib2.urlopen(url).read()

if __name__ == "__main__":
    print proof("http://www.themoviedb.org/authenticate/641bf16c663db167c6cffcdff41126039d4445bf")
