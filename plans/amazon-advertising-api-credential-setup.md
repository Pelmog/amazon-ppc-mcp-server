# Amazon Advertising API Credential Setup Plan

## Overview
This document provides a comprehensive plan for setting up all required credentials on Amazon Seller Central to access and use the Amazon Advertising API.

## Phase 1: Amazon Seller Central Foundation

### 1. Create Professional Seller Account
- Sign up for Amazon Professional Selling Plan ($39.99/month)
- Complete business verification (tax information, bank account)
- Maintain active selling status with good performance metrics

### 2. Enable Advertising Services
- Access Advertising Console within Seller Central
- Set up at least one advertising campaign (required for API access)
- Ensure advertising account is active and in good standing

## Phase 2: Developer Registration

### 3. Register as SP-API Developer
- Navigate to Partner Network > Develop Apps in Seller Central
- Complete Developer Central registration
- Provide organization contact details and use case information
- Accept Amazon's developer agreements and policies

### 4. Create Developer Profile
- Specify required API data access permissions
- Document security controls and compliance measures
- Define application use cases and integration requirements

## Phase 3: Application Registration

### 5. Register Application in Developer Console
- Choose application type (Private vs Public)
- For private apps: Use self-authorization process
- Provide application details and redirect URIs
- Configure OAuth 2.0 settings

### 6. Obtain API Credentials
- Generate Client ID and Client Secret
- Configure redirect URIs for OAuth flow
- Note down application identifiers

## Phase 4: Amazon Advertising API Access

### 7. Apply for Advertising API Access
- Submit application through Amazon Advertising Developer Portal
- Provide business justification and use case documentation
- Wait for approval (can take several weeks)

### 8. Configure LWA (Login with Amazon)
- Set up Login with Amazon integration
- Configure OAuth 2.0 authorization flow
- Test authentication endpoints

## Phase 5: Implementation & Testing

### 9. Set Up Authentication Flow
- Implement OAuth 2.0 authorization code flow
- Handle access token and refresh token management
- Configure profile ID (scope) management

### 10. API Integration Testing
- Test profile listing endpoints
- Verify advertising data access
- Implement error handling and rate limiting

## Required Credentials Summary

| Credential | Source | Purpose |
|------------|--------|---------|
| Client ID | Application registration | OAuth client identification |
| Client Secret | Application registration | OAuth client authentication |
| Redirect URI | App setup configuration | OAuth callback endpoint |
| Profile ID | Advertising account | API scope/account identifier |
| Access Token | OAuth flow | API request authentication |
| Refresh Token | OAuth flow | Token renewal |

## Prerequisites

- ✅ Active Amazon Professional Seller account
- ✅ Active advertising campaigns
- ✅ Business verification completed
- ✅ Good account standing and performance metrics

## Timeline Expectations

- **Phase 1-2**: 1-2 days (account setup and verification)
- **Phase 3**: 1-2 days (application registration)
- **Phase 4**: 2-4 weeks (API access approval)
- **Phase 5**: 1-2 weeks (implementation and testing)

**Total estimated time**: 4-6 weeks

## Important Notes

1. **API Access Approval**: Amazon Advertising API access requires manual approval and can take several weeks
2. **Active Selling Requirement**: Must maintain active selling and advertising activities
3. **Business Verification**: Complete tax and business information verification is mandatory
4. **Rate Limiting**: Implement proper rate limiting and error handling in your application
5. **Sandbox Environment**: Consider using Amazon's sandbox environment for initial testing

## Next Steps

1. Begin with Phase 1 if you don't have an active Professional Seller account
2. Ensure you have active advertising campaigns before applying for API access
3. Prepare business justification documentation for API access application
4. Plan for the 4-6 week timeline when scheduling development milestones