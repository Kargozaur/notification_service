from fastapi import APIRouter, Depends, status, Response
from services.notification_service.notification_service import (
    NotificationService,
)
