import re
import os

input_file = 'db_full_audit.sql'
output_file = 'REPORTE_FINAL.html'

print(f"🚀 Procesando formato específico de MariaDB...")

html_head = """
<html><head><meta charset="utf-8">
<style>
    body { font-family: 'Segoe UI', sans-serif; background: #1a1a1a; color: #fff; padding: 20px; }
    .table-container { overflow-x: auto; background: #2d2d2d; border-radius: 10px; padding: 10px; }
    table { border-collapse: collapse; width: 100%; min-width: 1000px; }
    th { background: #00d4ff; color: #000; padding: 12px; text-align: left; position: sticky; top: 0; }
    td { padding: 10px; border-bottom: 1px solid #444; max-width: 250px; word-wrap: break-word; font-size: 13px; }
    tr:hover { background: #3d3d3d; }
    .img-cell { background: white; width: 180px; text-align: center; border-radius: 4px; }
    img { max-width: 150px; max-height: 80px; cursor: pointer; transition: 0.3s; }
    img:hover { transform: scale(2.5); position: relative; z-index: 10; border: 2px solid #00d4ff; }
</style></head><body>
<h1>Reporte de Auditoría - UT ITALCO</h1>
<div class="table-container"><table>
<thead><tr>
    <th>ID</th><th>Entidad</th><th>Nombre Completo</th><th>Email</th><th>Hash / Password</th><th>Tag</th><th>Estado</th><th>Documento</th><th>Firma</th>
</tr></thead><tbody>
"""

with open(output_file, 'w', encoding='utf-8') as out:
    out.write(html_head)
    count = 0
    
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Buscamos patrones que empiecen por ( y tengan data:image dentro
            if 'data:image' in line:
                # Extraemos los bloques entre paréntesis
                rows = re.findall(r"\((.*?)\)", line)
                for row in rows:
                    if 'data:image' not in row: continue
                    
                    out.write("<tr>")
                    # Separamos los campos respetando que las comas están fuera de las comillas
                    columns = re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", row)
                    
                    for col in columns:
                        val = col.strip().strip("'")
                        if 'data:image' in val:
                            out.write(f'<td class="img-cell"><img src="{val}" onclick="window.open(this.src)"></td>')
                        else:
                            # Cortamos el hash largo para que no ensanche la tabla
                            display_val = (val[:20] + '...') if len(val) > 40 else val
                            out.write(f'<td>{display_val}</td>')
                    
                    out.write("</tr>")
                    count += 1
                    if count % 20 == 0:
                        print(f"📊 Registros procesados: {count}", end='\r')

    out.write("</tbody></table></div></body></html>")

print(f"\n\n✨ ¡LOGRADO! Se extrajeron {count} registros completos.")
print(f"📂 Abre 'REPORTE_FINAL.html' en tu navegador.")
