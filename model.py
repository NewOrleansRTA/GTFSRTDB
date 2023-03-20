from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, BigInteger
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

# Collapsed types:
# TripUpdate.trip
# TripUpdate.vehicle
# StopTimeUpdate.arrival
# StopTimeUpdate.departure
# Alert.active_period
# Position.latitude
# Position.longitude
# Position.bearing
# Position.speed
# VehicleDescriptor.id
# VehicleDescriptor.label
# VehicleDescriptor.license_plate

# The oid is called oid because several of the GTFSr types have string ids

class TripUpdate(Base):
    __tablename__ = 'trip_updates'
    oid = Column(Integer, primary_key=True)

    # This replaces the TripDescriptor message
    # TODO: figure out the relations
    trip_id = Column(String(32))
    route_id = Column(String(32))
    trip_start_time = Column(String(32))
    trip_start_date = Column(String(32))
    # Put in the string value not the enum
    # TODO: add a domain
    schedule_relationship = Column(String(32))

    # Collapsed VehicleDescriptor
    vehicle_id = Column(String(40))
    vehicle_label = Column(String(60))
    vehicle_license_plate = Column(String(32))

    # moved from the header, and reformatted as datetime
    timestamp = Column(DateTime(timezone=True))
    

    StopTimeUpdates = relationship('StopTimeUpdate', backref='TripUpdate')
    
class StopTimeUpdate(Base):
    __tablename__ = 'stop_time_updates'
    oid = Column(BigInteger, primary_key=True)

    stop_sequence = Column(Integer)
    stop_id = Column(String(32))

    # Collapsed StopTimeEvent
    arrival_delay = Column(Integer)
    arrival_time = Column(DateTime(timezone=True))
    arrival_uncertainty = Column(Integer)

    # Collapsed StopTimeEvent
    departure_delay = Column(Integer)
    departure_time = Column(DateTime(timezone=True))
    departure_uncertainty = Column(Integer)

    schedule_relationship = Column(String(32))

    # Link it to the TripUpdate
    trip_update_id = Column(Integer, ForeignKey('trip_updates.oid'))
    
    # The .TripUpdate is done by the backref in TripUpdate

class Alert(Base):
    __tablename__ = 'alerts'

    oid = Column(Integer, primary_key=True)

    # Collapsed TimeRange
    # start = Column(Integer)
    # end = Column(Integer)    

    # Add domain
    cause = Column(String(20))
    effect = Column(String(20))

    url = Column(String(300))
    header_text = Column(String(200))
    description_text = Column(String(4000))

    InformedEntities = relationship('EntitySelector', backref='Alert')

    # moved from the header, and reformatted as datetime
    timestamp = Column(DateTime(timezone=True))
    

class EntitySelector(Base):
    __tablename__ = 'entity_selectors'
    oid = Column(Integer, primary_key=True)

    agency_id = Column(String(32))
    route_id = Column(String(32))
    route_type = Column(Integer)
    stop_id = Column(String(32))

    # Collapsed TripDescriptor
    trip_id = Column(String(32))
    trip_route_id = Column(String(32))
    trip_start_time = Column(String(32))
    trip_start_date = Column(String(32))

    alert_id = Column(Integer, ForeignKey('alerts.oid'))

class VehiclePosition(Base):
    __tablename__ = 'vehicle_positions'
    oid = Column(BigInteger, primary_key=True)

    # This replaces the TripDescriptor message
    trip_id = Column(String(32))
    route_id = Column(String(32))
    trip_start_time = Column(String(15))
    trip_start_date = Column(String(15))
    schedule_relationship = Column(String(32))
 
    # Collapsed VehicleDescriptor
    vehicle_id = Column(String(300))
    vehicle_label = Column(String(300))
    vehicle_license_plate = Column(String(15))

    # Collapsed Position
    position_latitude = Column(Float)
    position_longitude = Column(Float)
    position_bearing = Column(Float)
    position_speed = Column(Float)
    position_timestamp = Column(DateTime(timezone=True))
    congestion_level = Column(String(60))
    occupancy_status = Column(String(60))

    # Extended Vehicle Descriptor
    # air_conditioned = Column(Boolean)
    # wheelchair_accessible = Column(Integer)
    # vehicle_model = Column(String(150))
    # special_vehicle_attributes = Column(Float)

    # moved from the header, and reformatted as datetime
    timestamp = Column(DateTime(timezone=True))
    
   

# So one can loop over all classes to clear them for a new load (-o option)
AllClasses = (TripUpdate, StopTimeUpdate, Alert, EntitySelector, VehiclePosition)
