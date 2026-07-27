# Generador de correos y contraseñas temporales

Aplicación de consola en Python que crea correos desechables reales (vía la API pública
de [mail.tm](https://mail.tm), sin necesidad de API key) y genera contraseñas seguras
de forma automática.

## Cómo abrirlo en VSCode

1. Descomprime la carpeta `temp-mail-app` en tu computador.
2. Ábrela en VSCode: `Archivo > Abrir carpeta...`
3. Abre una terminal integrada (`Ctrl + ñ` o `Terminal > Nueva terminal`).
4. (Opcional pero recomendado) Crea un entorno virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Linux/Mac
   ```
5. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
6. Ejecuta el programa:
   ```bash
   python main.py
   ```

## Qué hace

- Obtiene un dominio válido desde mail.tm.
- Genera un usuario y una contraseña aleatorios y seguros (usando el módulo `secrets`).
- Crea la cuenta de correo temporal mediante la API.
- Permite revisar la bandeja de entrada de esa cuenta desde la misma terminal.
- Permite generar cuantas cuentas temporales quieras dentro de la misma ejecución.

## Notas

- Las cuentas creadas en mail.tm son temporales y pueden expirar o eliminarse
  automáticamente pasado un tiempo (dependen del servicio, no de esta app).
- No se guarda ningún dato en disco; correo y contraseña solo se muestran en pantalla.
- Si quieres, puedo agregarle: guardar las cuentas generadas en un archivo, una interfaz
  gráfica (Tkinter) en vez de consola, o notificación automática cuando llegue un correo.
