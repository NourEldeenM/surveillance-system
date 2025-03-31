# import datetime
# from sqlalchemy.orm import Session
# from app.models.analytics import VisitorLog, Attendance
# from app.core.redis import redis_client

# class AnalyticsService:
#     @staticmethod
#     def record_visitor(db: Session, visitor_id: str, branch_id: str = None):
#         """
#         Records a visitor log in the database and increments a Redis counter.
#         """
#         visitor_log = VisitorLog(visitor_id=visitor_id, branch_id=branch_id)
#         db.add(visitor_log)
#         db.commit()
#         db.refresh(visitor_log)
        
#         # Update Redis counter (e.g., for overall visitor count or per branch)
#         redis_key = f"visitor_count:{branch_id}" if branch_id else "visitor_count:all"
#         redis_client.incr(redis_key)
        
#         return visitor_log

#     @staticmethod
#     def record_attendance(db: Session, employee_id: str, check_in: datetime.datetime, check_out: datetime.datetime = None):
#         """
#         Records an employee attendance log.
#         """
#         attendance = Attendance(employee_id=employee_id, check_in=check_in, check_out=check_out)
#         db.add(attendance)
#         db.commit()
#         db.refresh(attendance)
#         return attendance

#     @staticmethod
#     def get_dashboard_stats(db: Session):
#         """
#         Aggregates statistics for the dashboard:
#             - Total visitors (from Redis)
#             - Employee attendance count (from today's attendance records)
#         """
#         # Get visitor count from Redis
#         all_visitors = redis_client.get("visitor_count:all")
#         total_visitors = int(all_visitors) if all_visitors else 0

#         # Get today's attendance from the database
#         today = datetime.date.today()
#         start_of_day = datetime.datetime.combine(today, datetime.time.min)
#         attendance_today = db.query(Attendance).filter(Attendance.check_in >= start_of_day).all()
#         attended_employee_ids = {att.employee_id for att in attendance_today}
        
#         return {
#             "total_visitors": total_visitors,
#             "employee_attendance_today": len(attended_employee_ids)
#         }
