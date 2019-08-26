def make_phonetic(term):
    import re
    epithet = term.lower();  # ignore case
    epithet = epithet.replace("-", "");  # remove hyphen
    epithet = re.sub("c+([yie])", "z\\1", epithet);  # palatal c sounds like z
    epithet = re.sub("g([ie])", "j\\1", epithet);  # palatal g sounds like j
    epithet = re.sub("ph", "f", epithet);  # ph sounds like f
    epithet = epithet.replace("v", "f");  # v sounds like f # fricative (voiced or not)

    epithet = epithet.replace("h", "");  # h sounds like nothing
    epithet = re.sub("[gcq]", "k", epithet);  # g, c, q sound like k # guttural
    epithet = re.sub("[xz]", "s", epithet);  # x, z sound like s
    epithet = epithet.replace("ae", "e");  # ae sounds like e
    epithet = re.sub("[yei]", "i", epithet);  # y, e, i: all sound like i
    epithet = re.sub("[ou]", "u", epithet);  # o, u: all sound like u

    # so we only have a, i, u
    epithet = re.sub("[aiu]([aiu])[aiu]*", "\\1", epithet);  # remove diphtongs
    epithet = re.sub("(.)\\1", "\\1", epithet);  # doubled letters sound like single
    return epithet
