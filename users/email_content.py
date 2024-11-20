from datetime import datetime


def reset_password_email_content(reset_url, username, site_name):
    """Generate password reset email template with spam-prevention best practices"""

    html_message = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333; margin: 0; padding: 0;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <!-- Company Header -->
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #2C3E50; margin: 0;">{site_name}</h1>
        </div>
        
        <!-- Main Content -->
        <div style="background-color: #ffffff; padding: 20px; border-radius: 5px;">
            <p>Dear {username},</p>
            
            <p>You are receiving this email because you requested a password reset for your account at {site_name}.</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}" 
                   style="background-color: #3498DB; 
                          color: #ffffff; 
                          padding: 12px 25px; 
                          text-decoration: none; 
                          border-radius: 5px; 
                          display: inline-block;
                          font-weight: bold;">
                    Reset Your Password
                </a>
            </div>
            
            <p>For security, this link will expire in 24 hours.</p>
            
            <p><strong>Didn't request this?</strong> If you didn't request a password reset, please ignore this email or contact our support team if you have concerns.</p>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #EAECEE;">
                <p>Best regards,<br>{site_name} Team</p>
            </div>
        </div>
        
        <!-- Footer -->
        <div style="text-align: center; margin-top: 20px; font-size: 0.8em; color: #7F8C8D;">
            <p>© {datetime.now().year} {site_name}. All rights reserved.</p>
            <p>This is a transactional email regarding your account security.</p>
            
        </div>
    </div>
</body>
</html>
"""
    return {
        "subject": f"{site_name} - Password Reset Request",
        "html_message": html_message,
    }
