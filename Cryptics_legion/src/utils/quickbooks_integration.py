"""
QuickBooks Online Integration
Handles OAuth2 authentication and expense synchronization with QBO
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import base64
from urllib.parse import urlencode


class QuickBooksIntegration:
    """QuickBooks Online API Integration"""
    
    # QBO OAuth2 Endpoints
    AUTH_URL = "https://appcenter.intuit.com/connect/oauth2"
    TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/tokens/bearer"
    API_BASE_URL = "https://quickbooks.api.intuit.com/v2/company"
    
    def __init__(self, client_id: str, client_secret: str, realm_id: str, refresh_token: str = ""):
        """
        Initialize QuickBooks integration
        
        Args:
            client_id: QBO App Client ID
            client_secret: QBO App Client Secret
            realm_id: Company ID in QuickBooks
            refresh_token: Optional refresh token for existing connections
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.realm_id = realm_id
        self.refresh_token = refresh_token
        self.access_token = None
        self.token_expires_at = None
        
    def get_auth_url(self, redirect_uri: str) -> str:
        """
        Generate OAuth2 authorization URL for user login
        
        Args:
            redirect_uri: Callback URL after authorization
            
        Returns:
            Authorization URL
        """
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "scope": "com.intuit.quickbooks.accounting",
            "redirect_uri": redirect_uri,
            "state": "security_token"
        }
        return f"{self.AUTH_URL}?{urlencode(params)}"
    
    def exchange_code_for_token(self, auth_code: str, redirect_uri: str) -> Tuple[bool, Dict]:
        """
        Exchange authorization code for access token
        
        Args:
            auth_code: Authorization code from OAuth callback
            redirect_uri: Redirect URL used in authorization
            
        Returns:
            Tuple of (success: bool, response: dict)
        """
        auth_string = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth_string}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri
        }
        
        try:
            response = requests.post(self.TOKEN_URL, headers=headers, data=data, timeout=10)
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                self.refresh_token = token_data.get("refresh_token")
                expires_in = token_data.get("expires_in", 3600)
                
                from datetime import timedelta
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                
                return True, {
                    "access_token": self.access_token,
                    "refresh_token": self.refresh_token,
                    "realm_id": self.realm_id,
                    "token_expires_at": self.token_expires_at.isoformat()
                }
            else:
                return False, {"error": response.text}
        except Exception as e:
            return False, {"error": str(e)}
    
    def refresh_access_token(self) -> Tuple[bool, Dict]:
        """
        Refresh expired access token using refresh token
        
        Returns:
            Tuple of (success: bool, response: dict)
        """
        if not self.refresh_token:
            return False, {"error": "No refresh token available"}
        
        auth_string = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth_string}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        
        try:
            response = requests.post(self.TOKEN_URL, headers=headers, data=data, timeout=10)
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                self.refresh_token = token_data.get("refresh_token", self.refresh_token)
                expires_in = token_data.get("expires_in", 3600)
                
                from datetime import timedelta
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                
                return True, {
                    "access_token": self.access_token,
                    "refresh_token": self.refresh_token,
                    "token_expires_at": self.token_expires_at.isoformat()
                }
            else:
                return False, {"error": response.text}
        except Exception as e:
            return False, {"error": str(e)}
    
    def _ensure_token_valid(self) -> bool:
        """Check if token is valid and refresh if needed"""
        if not self.access_token:
            return False
        
        if self.token_expires_at:
            from datetime import timedelta
            if datetime.now() >= self.token_expires_at - timedelta(minutes=5):
                success, _ = self.refresh_access_token()
                return success
        
        return True
    
    def get_company_info(self) -> Tuple[bool, Dict]:
        """
        Get QuickBooks company information to verify connection
        
        Returns:
            Tuple of (success: bool, company_info: dict)
        """
        if not self._ensure_token_valid():
            return False, {"error": "Token invalid or expired"}
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json"
        }
        
        query = "select * from CompanyInfo"
        url = f"{self.API_BASE_URL}/{self.realm_id}/query?query={requests.utils.quote(query)}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return True, data.get("QueryResponse", {})
            else:
                return False, {"error": response.text}
        except Exception as e:
            return False, {"error": str(e)}
    
    def get_expense_accounts(self) -> Tuple[bool, List[Dict]]:
        """
        Get list of expense accounts from QuickBooks
        
        Returns:
            Tuple of (success: bool, accounts: list)
        """
        if not self._ensure_token_valid():
            return False, []
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json"
        }
        
        query = "select * from Account where AccountType='Expense'"
        url = f"{self.API_BASE_URL}/{self.realm_id}/query?query={requests.utils.quote(query)}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                accounts = []
                for item in data.get("QueryResponse", {}).get("Account", []):
                    accounts.append({
                        "id": item.get("id"),
                        "name": item.get("Name"),
                        "code": item.get("AcctNum")
                    })
                return True, accounts
            else:
                return False, []
        except Exception as e:
            return False, []
    
    def create_expense(self, expense_data: Dict) -> Tuple[bool, Dict]:
        """
        Create an expense/bill in QuickBooks
        
        Args:
            expense_data: Dictionary with expense details
                - description: str
                - amount: float
                - category: str
                - account_id: str (QuickBooks Account ID)
                - vendor_name: str
                - date: str (YYYY-MM-DD)
                
        Returns:
            Tuple of (success: bool, response: dict)
        """
        if not self._ensure_token_valid():
            return False, {"error": "Token invalid or expired"}
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Create Bill in QuickBooks
        bill_json = {
            "Line": [
                {
                    "DetailType": "AccountBasedExpenseLineDetail",
                    "Amount": expense_data.get("amount", 0),
                    "Description": expense_data.get("description", ""),
                    "AccountBasedExpenseLineDetail": {
                        "AccountRef": {
                            "value": expense_data.get("account_id", "")
                        }
                    }
                }
            ],
            "TxnDate": expense_data.get("date", datetime.now().strftime("%Y-%m-%d")),
            "VendorRef": {
                "value": ""  # This would need vendor lookup/creation
            },
            "PrivateNote": f"Imported from Cryptics Legion - {expense_data.get('category', '')}"
        }
        
        url = f"{self.API_BASE_URL}/{self.realm_id}/bill"
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=bill_json,
                timeout=10
            )
            
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {"error": response.text}
        except Exception as e:
            return False, {"error": str(e)}
    
    def sync_expenses(self, expenses: List[Dict]) -> Tuple[int, List[str], List[int]]:
        """
        Sync multiple expenses to QuickBooks
        
        Args:
            expenses: List of expense dictionaries
            
        Returns:
            Tuple of (synced_count: int, errors: list, synced_ids: list)
        """
        synced_count = 0
        errors = []
        synced_ids = []
        
        for expense in expenses:
            success, response = self.create_expense(expense)
            
            if success:
                synced_count += 1
                if "id" in expense:
                    synced_ids.append(expense["id"])
            else:
                error_msg = response.get("error", "Unknown error")
                errors.append(f"{expense.get('description', 'Unknown')}: {error_msg}")
        
        return synced_count, errors, synced_ids
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test if connection to QuickBooks is valid
        Note: For initial setup without refresh token, this validates credentials format
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        # If we have a refresh token, try full connection
        if self.refresh_token:
            try:
                if self._ensure_token_valid():
                    success, response = self.get_company_info()
                    if success:
                        company_name = response.get("CompanyInfo", [{}])[0].get("CompanyName", "Unknown")
                        return True, f"✅ Connected to: {company_name}"
                    else:
                        return False, f"❌ Connection failed: {response.get('error', 'Unknown error')}"
            except Exception as e:
                return False, f"❌ Connection error: {str(e)}"
        
        # Validate credentials format for initial setup
        if not all([self.client_id, self.client_secret, self.realm_id]):
            return False, "❌ Missing required credentials"
        
        if len(self.client_id) < 10:
            return False, "❌ Client ID appears invalid (too short)"
        
        if len(self.realm_id) < 5:
            return False, "❌ Realm ID appears invalid (too short)"
        
        # Credentials look valid, but need OAuth completion
        return True, "✅ Credentials format valid. Complete OAuth to finish connection."
    
    def validate_credentials(self) -> Tuple[bool, str]:
        """
        Simple validation of credential format (no API call)
        Good for initial setup verification
        """
        if not self.client_id or not self.client_secret or not self.realm_id:
            return False, "❌ All credentials are required"
        
        if len(self.client_id) < 10:
            return False, "❌ Client ID format invalid"
        
        if len(self.realm_id) < 5:
            return False, "❌ Realm ID format invalid"
        
        return True, "✅ All credentials appear valid!"
