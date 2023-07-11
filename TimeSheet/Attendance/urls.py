from django.urls import path
from Attendance import views

urlpatterns = [
    path('Details', views.attendance, name='attendance'),
    path('Details/<attendance_id>', views.attendance_Details, name='a_details1'),
    path('DetailsId', views.attendance_Details, name='a_details'),
    path('Attendance', views.make_attendance, name='makeattendance'),
    path('Leaves',views.getleave, name='leave'),
    path('RequestLeave', views.request_leave, name='requestLeave'),
    path('GetAttendance',views.getAttendance, name='getattendance'),
    path('getLeaves',views.getLeave,name='getLeave'),
    path('checkLeave',views.checkLeave,name="checkLeave"),
    #path('LeaveDetails/<leave_id>',views.LeaveDetails,name='LeaveDetails'),
    path('LeaveDetails',views.LeaveDetails,name='LeaveDetails'),
    path('updateLeave',views.updateLeave,name='updateLeave'),
    path('leaveCount',views.getLeaveCount, name='getLeaveCount'),
    path('attendanceCount',views.getattendanceCount, name='getAttendanceCount'),
    
    path('updateLeaveType',views.updateLeaveType, name="updateType"),
    path('getLeaveType',views.getLeaveType,name="getType"),
    path('getToday',views.getTodayAttendance,name='get_todays_attendance')
]
