# **Utveckling av ett ubåtsövervakningssystem med Python**
## **Beskrivning**
Detta projekt är ett Python-baserat system för att hantera ubåtar och deras data. Systemet kan:
-> Ladda och bearbeta rörelsedata för ubåtar.
-> Upptäcka kollisioner mellan ubåtar med tidsaspekt.
-> Kontrollera risk för "friendly fire" vid torpedavfyrning.
-> Analysera sensordata för att upptäcka fel.
-> Aktivera Nuke för ubåtar med säkerhetsvalidering.

## **Struktur**
Projektet är uppbyggt med följande moduler:
**`main.py`**: Huvudprogrammet som binder samman alla moduler och hanterar användarinteraktionen.
**`submarine.py`**: Innehåller klassen `Submarine` som hanterar ubåtens rörelser och status.
**`logger.py`**: Hanterar loggning av rörelser, fel och kollisioner.
**`sensor_data.py`**: Hanterar inläsning och analys av sensordata.
**`secret_manager.py`**: Hanterar säkerhetsaspekter som inläsning av hemliga nycklar och aktiveringskoder.

## **Installation och Körning**
1. **Krav**:
   -> Python 3.x
2. **Klona repositoriet** 
   - Se till att följande mappar finns i projektets rotkatalog:
     -> `MovementReports/`
     -> `Sensordata/`
     -> `Secrets/`
     -> `logs/` (skapas automatiskt när programmet körs)

3. **Datafiler**:
Här är länkarna till filerna som är lagrade på Google Drive:

- [Secrets](https://drive.google.com/file/d/15PeR3Rv4FJbvCu8w87-iX2ml59GutgWP/view?usp=sharing)
- [Sensordata](https://drive.google.com/file/d/1hkyoC2iR_Z6FXcz4nlGzpmwWD1IlU3il/view?usp=sharing)
- [MovementReports](https://drive.google.com/file/d/1potInXCTfjOijqXRo3XNL0_NwhbkhI0C/view?usp=sharing)

4. **Körning**:
   -> Öppna en terminal och navigera till projektets rotkatalog.
   -> Kör programmet 
## **Användning av programmet**
-> **Välj en ubåt** genom att ange serienummer när programmet frågar efter det.
-> **Bearbeta andra ubåtar** för att kontrollera kollisioner och torpedrisk.
-> **Analysera sensordata** för den valda ubåten för att upptäcka eventuella fel.
-> **Aktivera Nuke** för ubåten med korrekt säkerhetsvalidering genom att följa programmets instruktioner.