<!-- @format -->

Based on the provided OpenAPI Specification for the Amazon Advertising API v3.0 (labeled as v1 Beta in the paths), the API offers comprehensive functionality for programmatic management of advertising entities. All operations are performed via POST requests and require OAuth2 authentication with the advertising::campaign_management scope.

The core functionality is organized around the following resource types:

### **Campaigns**

The API provides full lifecycle management for advertising campaigns.

- **Create Campaigns (/adsApi/v1/create/campaigns):** Allows for the creation of new campaigns in bulk.
- **Update Campaigns (/adsApi/v1/update/campaigns):** Enables bulk updates to existing campaigns. This functions as a PATCH operation, meaning only the specified fields are modified.
- **Delete Campaigns (/adsApi/v1/delete/campaigns):** Facilitates the bulk archiving or deletion of campaigns.
- **Query Campaigns (/adsApi/v1/query/campaigns):** Provides a sophisticated search functionality to retrieve campaigns using complex filters, such as by ID, name, state, or ad product.

### **Portfolios**

Portfolios, which are collections of campaigns, can also be managed.

- **Create Portfolios (/adsApi/v1/create/portfolios):** Allows for the creation of new portfolios.
- **Update Portfolios (/adsApi/v1/update/portfolios):** Enables updates to existing portfolios.
- **Query Portfolios (/adsApi/v1/query/portfolios):** Allows users to search for and retrieve portfolios based on various filters.

### **Ad Groups**

These are the containers for ads within a campaign.

- **Create Ad Groups (/adsApi/v1/create/adGroups):** Supports the bulk creation of ad groups within specified campaigns.
- **Update Ad Groups (/adsApi/v1/update/adGroups):** Allows for bulk modifications to existing ad groups.
- **Delete Ad Groups (/adsApi/v1/delete/adGroups):** Permits the bulk archiving or deletion of ad groups.
- **Query Ad Groups (/adsApi/v1/query/adGroups):** Enables searching and retrieving ad groups using a variety of filters.

### **Ads**

This section covers the management of the actual ad creatives.

- **Create Ads (/adsApi/v1/create/ads):** Allows for the bulk creation of new ads within ad groups.
- **Update Ads (/adsApi/v1/update/ads):** Supports bulk updates to existing ads.
- **Delete Ads (/adsApi/v1/delete/ads):** Enables the bulk archiving or deletion of ads.
- **Query Ads (/adsApi/v1/query/ads):** Provides a way to search for and retrieve specific ads with complex filtering.

### **Targets**

Targeting determines where and when ads are shown.

- **Create Targets (/adsApi/v1/create/targets):** Allows for the bulk creation of new targeting expressions (e.g., keywords, products, audiences).
- **Update Targets (/adsApi/v1/update/targets):** Supports bulk updates to existing targets, such as changing bids or states.
- **Delete Targets (/adsApi/v1/delete/targets):** Enables the bulk archiving or deletion of targets.
- **Query Targets (/adsApi/v1/query/targets):** A search endpoint to retrieve targets using complex filters like target type, state, or associated campaign/ad group.

### **Ad Associations**

This appears to be a more specialized functionality, likely for DSP (Demand-Side Platform), managing relationships between ads.

- **Create Ad Associations (/adsApi/v1/create/adAssociations):** Creates new associations between ads.
- **Update Ad Associations (/adsApi/v1/update/adAssociations):** Modifies existing ad associations.
- **Delete Ad Associations (/adsApi/v1/delete/adAssociations):** Archives or deletes ad associations.
- **Query Ad Associations (/adsApi/v1/query/adAssociations):** Retrieves ad associations based on filters.

### **Key API Design Characteristics**

- **Bulk Operations:** All create, update, and delete operations are designed to handle requests in bulk, allowing for efficient management of multiple items in a single API call.
- **Multi-Status Responses:** For bulk operations (create, update, delete), the API uses a 207 Multi-Status response. This indicates that the server has processed the request and can return a mix of success and error messages for individual items within the batch.
- **Advanced Querying:** The query endpoints for each resource provide powerful, filter-based search capabilities, enabling more complex data retrieval than simple GET requests.
- **Authorization:** All actions require appropriate permissions (advertiser_campaign_edit or advertiser_campaign_view) and are scoped to a specific advertising account, which must be provided in the request headers (Amazon-Ads-AccountId).
- **Dual Account Types:** The API specifications indicate that it can be authorized for both standard Amazon Ads accounts (using a Profile ID) and DSP (Demand-Side Platform) accounts.
