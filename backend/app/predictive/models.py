"""Database models for Phase 117."""

from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, JSON
from app.database import Base


class SimulationModel(Base):
    __tablename__ = "predictive_simulations"

    id = Column(String, primary_key=True)
    scenario_hash = Column(String)
    status = Column(String)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class SimulationResultModel(Base):
    __tablename__ = "predictive_results"

    id = Column(String, primary_key=True)
    simulation_id = Column(String)
    result_json = Column(JSON)


class ForecastModel(Base):
    __tablename__ = "predictive_forecasts"

    id = Column(String, primary_key=True)
    attack_vector = Column(String)
    probability = Column(Float)
    time_window = Column(Integer)  # seconds
    created_at = Column(DateTime, default=datetime.utcnow)


class RiskScoreModel(Base):
    __tablename__ = "predictive_risk_scores"

    asset_id = Column(String, primary_key=True)
    score = Column(Float)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
