import os
def main():
    if not os.path.exists( "logs/" ):
        print("Creando carpeta de logs...")
        os.mkdir("logs/")

    if not os.path.exists( "data/" ):
        print("Creando carpeta de logs...")
        os.mkdir("data/")

    if not os.path.exists( "models/" ):
        print("Creando carpeta de logs...")
        os.mkdir("models/")

    if not os.path.exists( "notebooks/" ):
        print("Creando carpeta de logs...")
        os.mkdir("notebooks/")

    if not os.path.exists( "references/" ):
        print("Creando carpeta de logs...")
        os.mkdir("references/")

    if not os.path.exists( "reports/" ):
        print("Creando carpeta de logs...")
        os.mkdir("reports/")

    if not os.path.exists( "src/" ):
        print("Creando carpeta de logs...")
        os.mkdir("src/")

if __name__ == '__main__':
    main()