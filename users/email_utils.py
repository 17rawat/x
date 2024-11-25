from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


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


def verify_email_content(verify_email_url, username, site_name):
    html_message = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verify Your Email</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333; margin: 0; padding: 0;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <!-- Company Header -->
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #2C3E50; margin: 0;">{site_name}</h1>
        </div>
        
        <!-- Main Content -->
        <div style="background-color: #ffffff; padding: 20px; border-radius: 5px;">
            <p>Hello {username}!</p>
            
            <p>To verify your email address, please click the button below:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{verify_email_url}" 
                   style="background-color: #27AE60; 
                          color: #ffffff; 
                          padding: 12px 25px; 
                          text-decoration: none; 
                          border-radius: 5px; 
                          display: inline-block;
                          font-weight: bold;">
                    Verify Email Address
                </a>
            </div>
            
            <p>This link will expire in 24 hours for security reasons.</p>
            
            <p>If you did not create an account on {site_name} or did not request this verification, you can safely ignore this email.</p>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #EAECEE;">
                <p style="margin-bottom: 5px;">Best regards,</p>
                <p style="margin-top: 0;">{site_name} Team</p>
            </div>
        </div>
        
        
        <!-- Footer -->
        <div style="text-align: center; margin-top: 20px; font-size: 0.8em; color: #7F8C8D;">
            <p>© {datetime.now().year} {site_name}. All rights reserved.</p>
            <p style="margin-top: 5px;">This is an automated message, please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
"""

    return {
        "subject": f"Verify your email address - {site_name}",
        "html_message": html_message,
    }


def send_verification_email(request, user):
    try:
        # Generate verification tokens
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verify_email_url = request.build_absolute_uri(
            f"/users/verify-email/{uid}/{token}"
        )

        # Prepare email content
        email_content = verify_email_content(
            verify_email_url=verify_email_url,
            username=user.username,
            site_name=settings.SITE_NAME,
        )

        # Configure email message
        email_message = EmailMessage(
            subject=email_content["subject"],
            body=email_content["html_message"],
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
            reply_to=[settings.SUPPORT_EMAIL],
        )

        email_message.content_subtype = "html"
        email_message.extra_headers = {
            "List-Unsubscribe": f"<mailto:unsubscribe@{settings.SITE_DOMAIN}>",
            "X-Entity-Ref-ID": f"verify-email-{user.id}",
            "Precedence": "bulk",
        }

        # Send email and handle success
        email_message.send(fail_silently=False)
        messages.success(request, "Verification email has been sent to your email.")
        return True

    except Exception as e:
        # print("Error sending verification email:", e)
        # Log the error (you might want to add proper logging here)
        messages.error(
            request,
            "Failed to send verification email. Please try again later.",
        )
        return False
