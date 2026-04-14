import os
import gzip

# 1. Obtener la ruta absoluta de la carpeta donde está este script
directorio_donde_estoy = os.path.dirname(os.path.abspath(__file__))
# 2. Apuntar a la carpeta finca_base que está en ese mismo lugar
ruta_finca = os.path.join(directorio_donde_estoy, "tiles")

print("--- DIAGNÓSTICO ---")
print(f"Buscando en: {ruta_finca}")

if not os.path.exists(ruta_finca):
    print("❌ ERROR: No encuentro la carpeta 'finca_base' en esta ruta.")
    print("Asegúrate de que el script esté en la carpeta 'public' junto a 'finca_base'.")
else:
    print("✅ Carpeta encontrada. Buscando archivos .pbf...")
    
    conteo_total = 0
    conteo_reparados = 0

    for root, dirs, files in os.walk(ruta_finca):
        for file in files:
            if file.endswith(".pbf"):
                conteo_total += 1
                path = os.path.join(root, file)
                
                # Leer el archivo para ver si es Gzip
                with open(path, 'rb') as f:
                    inicio = f.read(2)
                
                # 1f 8b es la firma de un archivo Gzip
                if inicio == b'\x1f\x8b':
                    with gzip.open(path, 'rb') as f_in:
                        contenido_descomprimido = f_in.read()
                    with open(path, 'wb') as f_out:
                        f_out.write(contenido_descomprimido)
                    print(f"✨ Reparado: {file}")
                    conteo_reparados += 1

    print("--- RESUMEN ---")
    print(f"Archivos .pbf encontrados: {conteo_total}")
    print(f"Archivos que necesitaban reparación: {conteo_reparados}")