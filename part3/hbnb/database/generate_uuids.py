import uuid

# Generate UUID4s for amenities
# (admin UUID is already defined as fixed in the specifications)
wifi_uuid = uuid.uuid4()
pool_uuid = uuid.uuid4()
ac_uuid = uuid.uuid4()

print(f"UUID for WiFi: {wifi_uuid}")
print(f"UUID for Swimming Pool: {pool_uuid}")
print(f"UUID for Air Conditioning: {ac_uuid}")

# Display SQL instructions with the generated UUIDs
print("\nSQL instructions to insert into setup_db.sql:")
print(f"""
-- Insert initial amenities with generated UUID4 values
INSERT INTO amenities (id, name)
VALUES
    ('{wifi_uuid}', 'WiFi'),
    ('{pool_uuid}', 'Swimming Pool'),
    ('{ac_uuid}', 'Air Conditioning');
""")