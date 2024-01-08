import datetime
import typing
from string import Template


class Trie:
    """Regexp::Trie in python. Creates a Trie out of a list of words. The trie can be exported to a Regexp pattern.
    The corresponding Regexp should match much faster than a simple Regexp union."""

    #
    # author:         rex
    # blog:           http://iregex.org
    # filename        trie.py
    # created:        2010-08-01 20:24
    # source uri:     http://iregex.org/blog/trie-in-python.html

    # escape bug fix by fcicq @ 2012.8.19
    # python3 compatible by EricDuminil @ 2017.03.
    import re

    escape_table = {
        ".": "\\.",
        "?": ".",
        "-": "\\-",
        "*": "\\w+",
    }

    def __init__(self):
        self.data = {}

    def add(self, word):
        ref = self.data
        for char in word:
            ref[char] = char in ref and ref[char] or {}
            ref = ref[char]
        ref[""] = 1

    def dump(self):
        return self.data

    def quote(self, char):
        return Trie.escape_table.get(char) or Trie.re.escape(char)

    def _pattern(self, pData):
        data = pData
        if "" in data and len(data.keys()) == 1:
            return None

        alt = []
        cc = []
        q = 0
        for char in sorted(data.keys()):
            if isinstance(data[char], dict):
                try:
                    recurse = self._pattern(data[char])
                    alt.append(self.quote(char) + recurse)
                except:  # noqa: E722
                    cc.append(self.quote(char))
            else:
                q = 1
        cconly = not len(alt) > 0

        if len(cc) > 0:
            if len(cc) == 1:
                alt.append(cc[0])
            else:
                alt.append("[" + "".join(cc) + "]")

        if len(alt) == 1:
            result = alt[0]
        else:
            result = "(?:" + "|".join(alt) + ")"

        if q:
            if cconly:
                result += "?"
            else:
                result = "(?:%s)?" % result
        return result

    def pattern(self):
        return self._pattern(self.dump())


def read_and_order_hosts() -> typing.List[str]:
    headers = []
    hosts = set()

    with open("hosts.txt", "r+", encoding="utf-8") as fs:
        for line in fs:
            line = line.strip()

            if line.startswith("#"):
                headers.append(line)
            else:
                hosts.add(line)

        hosts = list(sorted(hosts))

        fs.truncate(0)
        fs.seek(0, 0)

        for line in headers:
            fs.write(line)
            fs.write("\n")

        for line in hosts:
            fs.write(line)
            fs.write("\n")

    return hosts


def build_regex(hosts: typing.List[str]) -> str:
    trie = Trie()
    for v in hosts:
        trie.add(v)

    return trie.pattern()


def build_ubl(hosts: typing.List[str]) -> str:
    lines = []
    trie = Trie()

    for x in hosts:
        if "?" in x or ("*" in x and not x.startswith("*")):
            trie.add(x)
        else:
            lines.append(f"*://{x}/*")

    lines.append(f"/^.*:\\/\\/{trie.pattern()}\\//")

    return "\n".join(lines)


def render(path: str, path_template: str, kargv: dict) -> str:
    with open(path_template, "r", encoding="utf-8") as fs:
        tmpl = Template(fs.read())

    with open(path, "w", encoding="utf-8") as fs:
        fs.truncate(0)
        fs.seek(0, 0)
        fs.write(tmpl.substitute(**kargv))


if __name__ == "__main__":
    now = (
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y.%m.%d.%H.%M")
        + " (UTC)"
    )

    hosts = read_and_order_hosts()
    regex = build_regex(hosts)
    ubl = build_ubl(hosts)

    kargv = {
        "NOW": now,
        "HOSTS": hosts,
        "REGEX": regex,
        "UBL": ubl,
    }

    render("only-stackoverflow.txt", "templates/only-stackoverflow.txt", kargv)
    render("ublacklist.txt", "templates/ublacklist.txt", kargv)
