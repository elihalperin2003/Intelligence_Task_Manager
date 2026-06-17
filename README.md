תיאור המערכת

המערכת מנהלת רשימת סוכנים ואת רשימת המשימות שלהם
המערכת עובדת לפי סט חוקים שמגדירים את כללי המשימות, הרשימה המלאה בהמשך
המערכת מאפשרת הוספת סוכנים ועדכון הפרטים שלהם וכן הוספת משימות ועדכון הסטטוס של המשימה
בכל שלב המערכת יכולה להציג את פרטי הסוכנים והמשימות שלהם וכן לתת סיכומים מסוימים כגון כמות משימות לפי סטטוס או כמות סוכנים ברמה מסוימת ועוד

----------------------------

מבנה התיקיות

```
intelligence-task-manager/
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore
```

----------------------------

מבנה הטבלאות

טבלת הסוכנים

id
INT, AUTO_INCREMENT, PRIMARY KEY

name
VARCHAR(50) NOT NULL

specialty
VARCHAR(50) NOT NULL

is_active
BOOLEAN	DEFAULT TRUE NOT NULL

completed_missions
INT	DEFAULT 0 NOT NULL

failed_mission
INT	DEFAULT 0 NOT NULL

agent_rank
ENUM (Junior / Senior / Commander) NOT NULL

---
טבלת המשימות

id
INT, AUTO_INCREMENT, PRIMARY KEY

title
VARCHAR(50) NOT NULL

description
TEXT NOT NULL

location
VARCHAR(50) NOT NULL

difficulty
INT NOT NULL

importance
INT NOT NULL

status
ENUM (NEW, ASSIGNED, IN_PROGRESS, COMPLETED, FAILED, CANCELLED) DEFAULT NEW NOT NULL

risk_level
VARCHAR NOT NULL
מחושב אוטומטית — לא מגיע מהמשתמש

assigned_agent_id
INT	NULL

----------------------------

הסבר על המחלקות

חוקים כלליים לכל המתודות

בכל מקום שלא נכתב במפורש מה להחזיר צריך להחזיר הודעת הצלחה או כישלון
כל מקום שצריך להחזיר רשימה אם לא נמצאו נתונים מחזיר רשימה ריקה

---
class DB_connection 

get_connection()
מחזירה חיבור פעיל ל-MySQL

create_database()
יוצרת את הדאטאבייס אם לא קיים

create_tables()
יוצרת את שתי הטבלאות אם לא קיימות

---
class AgentDB

create_agent(data)
יוצרת סוכן חדש ומחזירה את האובייקט של הסוכן

get_all_agents()
מחזירה רשימת כל הסוכנים

get_agent_by_id(id)
מחזירה סוכן אחד לפי ID, או None

update_agent(id, data)
UPDATE לכל השורה (אין אפשרות לשנות id)

deactivate_agent(id)
מגדירה מצב סוכן ללא פעיל

increment_completed(id)
מעלה ב1 את כמות המשימות שהושלמו

increment_failed(id)
מעלה ב1 את כמות המשימות שנכשלו

get_agent_performance(id)
מחזירה מילון עם המפתחות האלו
completed, failed, total, success_rate

count_active_agents()
מחזירה את מספר הסוכנים הפעילים 

---
class MissionDB

create_mission(data)
יצירת משימה חדשה ומחזירה את כל האובייקט

get_all_missions()
מחזירה את כל המשימות

get_mission_by_id(id)
מחזירה משימה אחת לפי ID, או None

assign_mission(m_id, a_id)
משייכת משימה לסוכן

update_mission_status(id, status)
משמשת לכל שינוי סטטוס

get_open_missions_by_agent(id)
מחזירה את המשימות של הסוכן במצבים האלה בלבד:
ASSIGNED/IN_PROGRESS

count_all_missions()
סה"כ משימות

count_by_status(status)
סופרת לפי סטטוס מסוים

count_open_missions()
סופרת משימות פתוחות

count_critical_missions()
סופרת משימות מסוג CRITICAL

get_top_agent()
מחזירה את הסוכן עם מספר המשימות שהושלמו הגבוה ביותר

----------------------------

חוקי המערכת

1
דרגת הסוכן חייבת להיות אחד מהרשימה הבאה
Junior / Senior / Commander

2
difficulty & importance
חייבים להיות בין 1 ל-10 — אחרת שגיאה

3
risk_level מחושב אוטומטית בעת יצירת משימה — המשתמש לא שולח אותו

4
סוכן לא פעיל לא יכול לקבל משימות

5
סוכן לא יכול להחזיק יותר משלוש משימות פתוחות במקביל
משימות פתוחות:
ASSIGNED / IN_PROGRESS

6
רק סוכן בדרגת קומנדור יכול לקבל את המשימה
CRITICAL

7
ניתן לשייך רק משימה במצב חדש

8
ניתן להתחיל לבצע משימה רק במצב רשום

9
ניתן לסווג ולסיים משימה כהושלמה או כנכשלה רק כשהמשימה בפעולה

10
ניתן לבטל משימה רק בשלב הפתיחה והשייוך אך לא בשעת ביצוע המשימה

----------------------------

הוראות הרצה

docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
  -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0

