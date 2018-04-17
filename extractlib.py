import re
import sys

#get basic url format counting a few obfuscation techniques
GENERIC_URL_RE = re.compile(r"\b[ht]\w\w?ps?[\:\_]\/\/\S+\b")
#if we know hxxp then auto get all of that
HXXP_URL_RE = re.compile(r"\bhxxps?\:\/\/\S+\b")
#get some obfuscated ip addresses
IP_RE = re.compile(r"(\d{1,3}\[?\.\]?\d{1,3}\[?\.\]?\d{1,3}\[?\.\]?\d{1,3}(?:\/\d{1,3})?)")

EMAIL_RE = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
MD5_RE = re.compile(r"(\b[a-fA-F\d]{32})\b")
SHA1_RE = re.compile(r"\b([a-fA-F\d]{40})\b")
SHA256_RE = re.compile(r"\b([a-fA-F\d]{64})\b")
SHA512_RE = re.compile(r"(\b[a-fA-F\d]{128})\b")

def extract_info(data, generic_urls=False, hxxp_urls=False, ips=False, emails=False, hashes=False):
    """
    Gets desired data from string using various regex
    """

    #if select nothing then run all
    if not generic_urls and not hxxp_urls and not ips and not hashes and not emails:
        generic_urls = ips = hashes = emails = True

    if generic_urls:
        for url in GENERIC_URL_RE.findall(data):
            yield(url)

    if hxxp_urls:
        for url in HXXP_URL_RE.findall(data):
            yield(url)

    if ips:
        for ip in IP_RE.findall(data):
            yield(ip)

    if emails:
        for email in EMAIL_RE.findall(data):
            yield(email)

    if hashes:
        for md5 in MD5_RE.findall(data):
            yield(md5)
        for sha1 in SHA1_RE.findall(data):
            yield(sha1)
        for sha256 in SHA256_RE.findall(data):
            yield(sha256)
        for sha512 in SHA512_RE.findall(data):
            yield(sha512)

def extract_yara_rules(text):
    yara_rules = re.sub("\n[\t\s]*\}[\s\t]*(rule[\t\s][^\r\n]+(?:\{|[\r\n][\r\n\s\t]*\{))", "}\r\n\\1", text,
                        re.MULTILINE | re.DOTALL)
    yara_rules = re.compile(
        r"^[\t\s]*rule[\t\s][^\r\n]+(?:\{|[\r\n][\r\n\s\t]*\{).*?condition:.*?\r?\n?[\t\s]*\}[\s\t]*(?:$|\r?\n)",
        re.MULTILINE | re.DOTALL).findall(yara_rules)
    extracted = []
    for yara_rule in yara_rules:
        try:
            extracted.append(parse_yara_rules_text(yara_rule)[0])
        except:
            pass

    return extracted
