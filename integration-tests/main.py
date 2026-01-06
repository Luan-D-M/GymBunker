import requests
import sys

def main():
    # --- Configuration ---
    BASE_URL = "http://localhost:5000"
    USERNAME = "testuser"
    PASSWORD = "password123"

    print(f"🚀 Starting integration tests on {BASE_URL}...")

    try:
        # 1. Test Health / Connectivity
        print("1. Testing Service Connectivity...", end=" ")
        try:
            resp = requests.get(f"{BASE_URL}/") # Or /health
            # Accept 200 OK or 404 (which means server is up but route is missing)
            assert resp.status_code in [200, 404], f"Server returned bad status: {resp.status_code}"
            print("✅ OK")
        except requests.exceptions.ConnectionError:
            print("\n❌ FAILED: Could not connect to server. Is it running?")
            sys.exit(1)

        # 2. Test Sign Up
        print("2. Testing Sign Up...", end=" ")
        signup_payload = {
            "username": USERNAME,
            "password": PASSWORD
        }
        
        resp = requests.post(f"{BASE_URL}/signup", json=signup_payload)
        
        if resp.status_code == 409:
            print("⚠️  User already exists (Skipping creation)", end=" ")
        else:
            # Accept 200 or 201 (Created)
            assert resp.status_code in [200, 201], f"Sign Up failed: {resp.status_code} - {resp.text}"
        print("✅ OK")

        # 3. Test Login & Token Issuance
        print("3. Testing Login Flow...", end=" ")
        login_payload = {
            "username": USERNAME,
            "password": PASSWORD
        }
        
        # Note: If using OAuth2PasswordRequestForm, change `json=...` to `data=...`
        # and ensure the endpoint is correct (often /token).
        resp = requests.post(f"{BASE_URL}/login", json=login_payload)
        
        assert resp.status_code == 200, f"Login failed: {resp.status_code} - {resp.text}"
        
        data = resp.json()
        assert "access_token" in data, "No 'access_token' in response"
        token = data["access_token"]
        print("✅ OK")

        # 4. Verify Token Structure (Basic Check)
        print("4. Verifying Token Structure...", end=" ")
        parts = token.split('.')
        assert len(parts) == 3, "Token does not look like a valid JWT (Header.Payload.Signature)"
        print("✅ OK")

        # 5. Test Public Key Endpoint (Optional)
        print("5. Testing Public Key Endpoint...", end=" ")
        resp = requests.get(f"{BASE_URL}/public-key") 
        
        if resp.status_code == 404:
            print("⚠️  SKIPPED (Endpoint not found)")
        else:
            assert resp.status_code == 200, f"Failed to get key: {resp.status_code}"
            assert "-----BEGIN PUBLIC KEY-----" in resp.text, "Response does not contain a PEM key"
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