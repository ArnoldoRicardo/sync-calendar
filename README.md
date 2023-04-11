# what is this

this couple of script for clone the outlook events to google calendar

## how to run

firts you need download the outlook events

```
    python scraper.py
```

this script will create a events.db database

and then you need upload this events to google calendar


```
    python upload_events.py
```


## scraper de windows application

python outlook_win32.py

### schedule

for schedule outlook_win32 you need to use download_calendar.bat

Abra PowerShell como administrador.

Ejecute el siguiente comando para crear una nueva tarea programada:

```
New-ScheduledTaskTrigger -Daily -At 9am -DaysInterval 1
```

Este comando creará una tarea programada diaria que se ejecutará a las 9am.

Ejecute el siguiente comando para agregar una acción a la tarea programada:

```
$action = New-ScheduledTaskAction -Execute 'C:\ruta\a\su\download_calendar.bat'
Register-ScheduledTask -TaskName "Nombre de la tarea" -Action $action
```

Reemplace "Nombre de la tarea" con un nombre descriptivo para su tarea programada y "C:\ruta\a\su\download_calendar.bat" con la ruta completa a su archivo .bat.

Verifique que la tarea programada se haya creado correctamente ejecutando el siguiente comando:

```
Get-ScheduledTask -TaskName "Nombre de la tarea"
```

Este comando debería mostrar información sobre la tarea programada que acaba de crear.

Con estos pasos, habrá creado una tarea programada en su sistema que ejecutará su archivo .bat a las 9am todos los días. Si necesita hacer ajustes a la hora de ejecución o la frecuencia, puede cambiar los valores de los parámetros en el primer comando.

### get info

ejecutar la tarea
```
Start-ScheduledTask -TaskName "Outlook"
```

obtener informacion de la tarea
```
Get-ScheduledTaskInfo -TaskName "Outlook"
```