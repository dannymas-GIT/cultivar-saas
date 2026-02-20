# Cultivar - QA Test Specification

## Smoke Tests

### 1. Homepage loads
- Navigate to /
- Expect: Page renders with app title
- Expect: No console errors

### 2. API health check
- Navigate to /
- Expect: API status shows "connected" or equivalent
- Expect: Health indicator is green/success

## Prerequisites

Configure in ~/.openclaw/openclaw.env:
- CULTIVAR_SAAS_BASE_URL - Staging URL (e.g. http://appname.staging.yourdomain.com)
- CULTIVAR_SAAS_TEST_EMAIL - Test user email (if auth exists)
- CULTIVAR_SAAS_TEST_PASSWORD - Test user password (if auth exists)
