from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Index
from datetime import datetime

from core.database import Base


class EndpointStats(Base):
    """Table to store endpoint statistics"""
    __tablename__ = "endpoint_stats"

    id = Column(Integer, primary_key=True, index=True)
    endpoint_name = Column(String(255), nullable=False, index=True)
    method = Column(String(10), nullable=False)
    params = Column(JSON, nullable=True)
    params_hash = Column(String(64), nullable=False, index=True)
    total_calls = Column(Integer, default=0)
    last_called = Column(DateTime, default=datetime.utcnow)


    __table_args__ = (
        Index('idx_endpoint_params', 'endpoint_name', 'params_hash'),
        Index('idx_endpoint_method', 'endpoint_name', 'method'),
    )
