# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.orm import Session
# from app.services.analytics import AnalyticsService
# from app.core.database import SessionLocal
# from app.schemas.analytics import VisitorLogCreate, VisitorLogResponse, AttendanceCreate, AttendanceResponse
# import datetime

# router = APIRouter(prefix="/analytics", tags=["analytics"])

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/visitor", response_model=VisitorLogResponse)
# def record_visitor(visitor: VisitorLogCreate, db: Session = Depends(get_db)):
#     """
#     Endpoint to record a visitor event.
#     """
#     try:
#         visitor_log = AnalyticsService.record_visitor(db, visitor.visitor_id, visitor.branch_id)
#         return visitor_log
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/dashboard")
# def get_dashboard(db: Session = Depends(get_db)):
#     """
#     Endpoint to retrieve aggregated dashboard statistics.
#     """
#     try:
#         stats = AnalyticsService.get_dashboard_stats(db)
#         return stats
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.post("/attendance", response_model=AttendanceResponse)
# def record_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
#     """
#     Endpoint to record an employee attendance event.
#     """
#     try:
#         record = AnalyticsService.record_attendance(
#             db,
#             attendance.employee_id,
#             attendance.check_in,
#             attendance.check_out
#         )
#         return record
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
