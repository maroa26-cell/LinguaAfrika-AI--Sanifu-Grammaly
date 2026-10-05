def kagua_matini(matini):
    if not matini or matini.strip() == "":
        return False
    return True

def kagua_faili(faili):
    if faili is None:
        return False
    if faili.name.split('.')[-1] not in ['mp3', 'wav']:
        return False
    return True
