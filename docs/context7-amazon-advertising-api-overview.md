# Context7 Amazon Advertising API Overview

## Introduction

Context7 provides comprehensive documentation and code examples for Amazon Advertising API integration through two primary TypeScript/JavaScript SDKs. This document outlines all available functionality and capabilities exposed through Context7's understanding of the Amazon Advertising API.

## Available SDKs in Context7

### 1. ScaleLeap Amazon Advertising API SDK (`/scaleleap/amazon-advertising-api-sdk`)
- **Trust Score**: 8.5/10
- **Code Snippets**: 15
- **Language**: TypeScript/Node.js
- **Focus**: Core Amazon Advertising API operations

### 2. Whitebox Amazon Ads API (`/whitebox-co/amazon-ads-api`)
- **Trust Score**: 5.8/10  
- **Code Snippets**: 16
- **Language**: TypeScript/Node.js
- **Focus**: Advanced client management and auto-generated API clients

## Core Functionality Available

### Authentication & Authorization

#### OAuth 2.0 Flow Management
```typescript
// OAuth client initialization
const client = new OAuthClient({
  clientId: '...',
  clientSecret: '...',
  redirectUri: '...'
}, amazonMarketplaces.US)

// Authorization URI generation
const uri = client.getUri()

// Token management
const token = client.getToken()
const refreshedToken = await token.refresh()
```

#### HTTP Client Configuration
```typescript
// Basic authentication setup
const auth = {
  accessToken: "ACCESS_TOKEN",
  clientId: "YOUR_CLIENT_ID",
  scope: 10000000000 // Profile ID
}
const httpClient = new HttpClient('https://advertising-api.amazon.com', auth)
```

### API Client Architecture

#### ScaleLeap SDK Architecture
1. **HttpClient**: Core HTTP communication layer
2. **OperationProvider**: Factory for creating operation instances
3. **Operation Classes**: Specific API endpoint handlers (e.g., ProfileOperation)
4. **AmazonAdvertising**: High-level wrapper class

#### Whitebox SDK Architecture
1. **AmazonAds Class**: Central credential and configuration management
2. **Auto-generated Clients**: Dynamically generated from OpenAPI schemas
3. **Attribution Client**: Specialized attribution API handling
4. **Built-in Rate Limiting**: Advanced throttling and retry mechanisms

### Profile Management

#### Profile Operations
```typescript
// List advertising profiles
const profileOperation = operationProvider.create(ProfileOperation)
const profiles = await profileOperation.listProfiles()

// Using AmazonAdvertising class
const amazonAdvertising = new AmazonAdvertising(amazonMarketplaces.US, auth)
const profileResults = await amazonAdvertising.profile.listProfiles()
```

### Advanced Client Features (Whitebox SDK)

#### Rate Limiting & Throttling
```typescript
const configuration = {
    throttling: {
        reservoir: 100,
        reservoirRefreshAmount: 100,
        reservoirRefreshInterval: 60 * 1000,
        maxConcurrent: 5,
        minTime: 333,
    },
    retries: {
        count: 3,
        refreshTime: 5000,
        maxWaitTime: 5000,
        retryCallback: (jobId: string) => { console.log(`Retrying job ${jobId}`); }
    }
}
```

#### Attribution API Support
```typescript
const attributionClient = await amazonAdsApi.getConfiguredApi(AttributionClient, credentials)
const response = await attributionClient.getAdvertisersByProfile({
    amazonAdvertisingAPIClientId: '',
    amazonAdvertisingAPIScope: ''
})
```

### Marketplace Support

#### Supported Amazon Marketplaces
- US (amazon.com)
- International marketplaces through `@scaleleap/amazon-marketplaces`
- Marketplace validation via `assertMarketplaceHasAdvertising()`

### Development & Testing Support

#### API Schema Management (Whitebox)
```bash
# Download latest API schemas
npm run download-schemas

# Generate models from schemas  
npm run generate-models

# Generate API clients
npm run generate-clients

# Complete API generation pipeline
npm run generate-apis
```

#### Documentation Generation
```bash
# Generate TypeDoc documentation
npm run docs

# Generate Redoc API documentation
npm run docs:redoc

# Generate SwaggerUI documentation
npm run docs:swaggerui
```

#### Testing & Development
```bash
# Development mode with live reload
npm run dev

# Run tests with filtering
npm test -- -i -t "Attribution"

# Linting
npm run lint
```

## API Capabilities Exposed

### Core Operations
1. **Profile Management**
   - List advertising profiles
   - Profile-scoped operations
   - Multi-marketplace support

2. **Authentication Management**
   - OAuth 2.0 flow handling
   - Token refresh automation
   - Credential caching

3. **HTTP Communication**
   - Configurable base URLs
   - Authentication header management
   - Request/response handling

### Advanced Features (Whitebox SDK)
1. **Auto-generated API Clients**
   - Dynamic client generation from OpenAPI schemas
   - Daily automated schema updates
   - Complete API coverage

2. **Rate Limiting & Resilience**
   - Configurable throttling
   - Automatic retries with backoff
   - Job queue management
   - Envoy proxy rate limiting support

3. **Attribution API**
   - Dedicated attribution client
   - Advertiser profile management
   - Attribution data retrieval

## Installation & Setup

### ScaleLeap SDK
```bash
npm install @scaleleap/amazon-advertising-api-sdk
```

### Whitebox SDK
```bash
npm install @whitebox-co/amazon-ads-api
```

## Configuration Options

### Basic Configuration
- Client credentials (ID, secret, redirect URI)
- Access tokens and refresh tokens
- Profile ID (scope)
- Marketplace selection

### Advanced Configuration (Whitebox)
- Throttling parameters
- Retry policies
- Job expiration settings
- Proxy rate limiting
- Custom callback functions

## Development Workflow Support

### Code Generation Pipeline
1. **Schema Download**: Fetch latest OpenAPI specifications
2. **Model Generation**: Create TypeScript models from schemas
3. **Client Generation**: Generate API client classes
4. **Documentation**: Auto-generate API documentation

### Testing Support
- PollyJS recording support for API interactions
- Automated CI/CD integration
- Test filtering and debugging capabilities

## Key Strengths

### ScaleLeap SDK
- Clean, intuitive API design
- Strong TypeScript support
- Comprehensive OAuth handling
- Well-documented code examples

### Whitebox SDK  
- Comprehensive API coverage via auto-generation
- Advanced rate limiting and resilience
- Attribution API specialization
- Extensive development tooling

## Use Cases Supported

1. **Basic Amazon Advertising Integration**
   - Profile management
   - Authentication handling
   - Simple API operations

2. **Enterprise-Grade Applications**
   - Advanced rate limiting
   - High-volume API usage
   - Multiple client management
   - Robust error handling

3. **Attribution Analytics**
   - Attribution data collection
   - Advertiser performance analysis
   - Cross-platform attribution tracking

4. **Development & Testing**
   - API exploration and testing
   - Documentation generation
   - Schema management and updates

## Limitations & Considerations

1. **API Coverage**: While extensive, may not cover all Amazon Advertising API endpoints
2. **Marketplace Support**: Primarily focused on major marketplaces
3. **Version Management**: Requires attention to API version updates
4. **Rate Limiting**: Must be configured appropriately for production use

## Conclusion

Context7 provides comprehensive support for Amazon Advertising API integration through two complementary SDKs. The ScaleLeap SDK offers clean, straightforward API access, while the Whitebox SDK provides enterprise-grade features with auto-generated clients and advanced resilience patterns. Together, they cover the full spectrum of Amazon Advertising API development needs, from simple integrations to complex, high-volume applications.