import io


def deobfusquer(fichier_entree: str):
    """Obfusquer les fichiers pour les protéger contre les robots ou certains profs de NSI qui devront découvrir d'eux-mêmes hehe"""
    with open(fichier_entree, 'rb') as f:
        data = f.read()
    # Inverser les données pour les déobfusquer
    data_deobfusquee = data[::-1]
    return io.BytesIO(data_deobfusquee)
