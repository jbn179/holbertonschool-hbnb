import uuid

# Générer des UUID4 pour les commodités
# (admin UUID est déjà défini comme fixe dans les spécifications)
wifi_uuid = uuid.uuid4()
pool_uuid = uuid.uuid4()
ac_uuid = uuid.uuid4()

print(f"UUID pour WiFi: {wifi_uuid}")
print(f"UUID pour Swimming Pool: {pool_uuid}")
print(f"UUID pour Air Conditioning: {ac_uuid}")

# Afficher les instructions SQL avec les UUID générés
print("\nInstructions SQL à insérer dans setup_db.sql:")
print(f"""
-- Insert initial amenities with generated UUID4 values
INSERT INTO amenities (id, name)
VALUES
    ('{wifi_uuid}', 'WiFi'),
    ('{pool_uuid}', 'Swimming Pool'),
    ('{ac_uuid}', 'Air Conditioning');
""")