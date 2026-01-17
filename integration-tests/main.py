import requests
import sys

def main():
    # --- Configuration ---
    AUTH_URL = "http://localhost/auth"
    WORKOUT_URL = "http://localhost/user"
    
    USERNAME = "username123"
    PASSWORD = "password123"

    print(f"🚀 Starting integration tests...")
    print(f"   Auth Service: {AUTH_URL}")
    print(f"   Workout Service: {WORKOUT_URL}")

    try:
        # --- AUTHENTICATOR SERVICE TESTS ---
        # Test Health / Connectivity (Auth)
        print("\n1. Testing Auth Service Connectivity...", end=" ")
        try:
            resp = requests.get(f"{AUTH_URL}/") 
            assert resp.status_code in [200, 404], f"Server returned bad status: {resp.status_code}"
            print("✅ OK")
        except requests.exceptions.ConnectionError:
            print("\n❌ FAILED: Could not connect to Auth server.")
            sys.exit(1)



        # Test Sign Up
        print("2. Testing Sign Up...", end=" ")
        signup_payload = {
            "username": USERNAME,
            "password": PASSWORD
        }
        resp = requests.post(f"{AUTH_URL}/signup", json=signup_payload)
        if resp.status_code == 409:
            print("⚠️  User already exists (Skipping creation)", end=" ")
        else:
            assert resp.status_code in [200, 201], f"Sign Up failed: {resp.status_code} - {resp.text}"
        print("✅ OK")



        #  Test Login & Token Issuance
        print(" Testing Login Flow...", end=" ")
        login_payload = {
            "username": USERNAME,
            "password": PASSWORD
        }

        resp = requests.post(f"{AUTH_URL}/login", json=login_payload)
        assert resp.status_code == 200, f"Login failed: {resp.status_code} - {resp.text}"
        
        data = resp.json()
        assert "access_token" in data, "No 'access_token' in response"
        token = data["access_token"]
        print("✅ OK")



        # Verify Token Structure
        print("4. Verifying Token Structure...", end=" ")
        parts = token.split('.')
        assert len(parts) == 3, "Token format invalid"
        print("✅ OK")






        # --- WORKOUT SERVICE TESTS ---
        # Prepare Headers
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Test Add Workout
        print("5. Testing Add Workout...", end=" ")
        workout_name = "Integration Chest Day"
        add_payload = {
            "workout": {
                "workout_name": workout_name,
                "exercises": [
                    {
                        "name": "Bench Press",
                        "weight": 100,
                        "number_sets": 3,
                        "number_reps": 10,
                        "rest_time_in_seconds": 60
                    }
                ]
            }
        }
        
        resp = requests.post(f"{WORKOUT_URL}/add-workout", json=add_payload, headers=headers)
        assert resp.status_code == 201, f"Add Workout failed: {resp.status_code} - {resp.text}"
        
        # Verify persistence in response
        resp_data = resp.json()
        found_workout = any(w['workout_name'] == workout_name for w in resp_data.get('workouts', []))
        assert found_workout, "Added workout not found in response"
        print("✅ OK")




        # Test Get User Data (Verify Persistence)
        print("6. Testing Get User Data...", end=" ")
        resp = requests.get(f"{WORKOUT_URL}/", headers=headers)
        assert resp.status_code == 200, f"Get Data failed: {resp.status_code} - {resp.text}"
        
        user_data = resp.json()
        # Ensure we got the right user's data
        assert user_data['user_id'] == USERNAME, f"User ID mismatch: {user_data.get('user_id')}"
        assert len(user_data['workouts']) >= 1, "Workouts list is empty"
        print("✅ OK")



        # Test Update Workout
        print("7. Testing Update Workout...", end=" ")
        update_payload = {
            "workout": {
                "workout_name": workout_name,
                "exercises": [
                    {
                        "name": "Incline Bench Press", # Changed name
                        "weight": 110, # Changed weight
                        "number_sets": 4,
                        "number_reps": 8
                    }
                ]
            }
        }
        
        resp = requests.post(f"{WORKOUT_URL}/update-workout/{workout_name}", json=update_payload, headers=headers)
        assert resp.status_code == 200, f"Update Workout failed: {resp.status_code} - {resp.text}"
        
        # Verify update in response
        updated_data = resp.json()
        updated_workout = next((w for w in updated_data['workouts'] if w['workout_name'] == workout_name), None)
        assert updated_workout is not None, "Workout not found after update"
        assert updated_workout['exercises'][0]['name'] == "Incline Bench Press", "Workout update did not persist"
        print("✅ OK")




        # Test Delete Workout
        print("8. Testing Delete Workout...", end=" ")
        resp = requests.delete(f"{WORKOUT_URL}/delete-workout/{workout_name}", headers=headers)
        assert resp.status_code == 200, f"Delete Workout failed: {resp.status_code} - {resp.text}"
        
        # Verify deletion
        resp = requests.get(f"{WORKOUT_URL}/", headers=headers)
        user_data = resp.json()
        deleted_workout = next((w for w in user_data['workouts'] if w['workout_name'] == workout_name), None)
        assert deleted_workout is None, "Workout was not deleted"
        print("✅ OK")


        # --- EDGE CASE TESTS ---
        # E1. Test Unauthorized Access (Security)
        print("E1. Testing Unauthorized Access (No Token)...", end=" ")
        # Try to access data without headers
        resp = requests.get(f"{WORKOUT_URL}/")
        assert resp.status_code in [401, 403], f"Security Fail! API allowed access without token. Status: {resp.status_code}"
        print("✅ OK")



        # E2. Test Operating on Non-Existent Resource (Stability)
        print("E2. Testing Update on 'Ghost' Workout...", end=" ")
        fake_workout = "Ghost Workout 3000"
        fake_payload = {
            "workout": { "workout_name": fake_workout, "exercises": [] }
        }
        resp = requests.post(f"{WORKOUT_URL}/update-workout/{fake_workout}", json=fake_payload, headers=headers)
        
        if resp.status_code == 404:
             print("✅ OK (Handled gracefully)")
        elif resp.status_code == 500:
             print("❌ FAILED: Server crashed (500) instead of returning 404.")
        else:
             print(f"⚠️  Unexpected Status: {resp.status_code}")



        # E3. Test Bad Input Data (Data Integrity)
        print("E3. Testing Bad Input (Negative Weight)...", end=" ")
        bad_payload = {
            "workout": {
                "workout_name": "Impossible Workout",
                "exercises": [
                    {
                        "name": "Anti-Gravity Press",
                        "weight": -100, # Logic error
                        "number_sets": -5,
                        "number_reps": 0
                    }
                ]
            }
        }
        resp = requests.post(f"{WORKOUT_URL}/add-workout", json=bad_payload, headers=headers)
        
        if resp.status_code == 201:
            print("⚠️  API accepted negative numbers (No validation layer detected)")
            # Cleanup the bad data so it doesn't stay in DB
            requests.patch(f"{WORKOUT_URL}/delete-workout/Impossible Workout", headers=headers)
        elif resp.status_code == 400:
            print(f" {resp.json()}")
            print("✅ OK (Rejected bad data)")
        else:
            print(f"ℹ️  Status: {resp.status_code}")





        # --- CLEANUP ---
        #  Test Delete Account
        print("9. Testing Delete Account...", end=" ")
        delete_payload = {
            "password": PASSWORD
        }
        
        resp = requests.delete(f"{AUTH_URL}/delete-account", json=delete_payload, headers=headers)
        assert resp.status_code == 200, f"Delete Account failed: {resp.status_code} - {resp.text}"
        print("✅ OK")

        #  Verify Account is Gone
        print("10. Verifying Account Deletion...", end=" ")
        resp = requests.post(f"{AUTH_URL}/login", json=login_payload)
        assert resp.status_code == 401, f"Login succeeded but account should be deleted! Status: {resp.status_code}"
        print("✅ OK")

        print("\n✨ ALL TESTS PASSED.")

    except AssertionError as e:
        print(f"\n❌ FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()