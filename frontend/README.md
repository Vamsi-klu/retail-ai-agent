# Retail AI Pro - Frontend

Enterprise-grade React frontend for the Retail AI Pro system.

## Features

- **React 18** with TypeScript
- **Vite** for blazing-fast development
- **Redux Toolkit** for state management
- **React Query** for server state management
- **Tailwind CSS** for styling
- **Vitest** for testing with 95%+ coverage
- **React Router** for navigation

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

The app will be available at http://localhost:3000

### Building

```bash
npm run build
```

### Testing

```bash
# Run tests
npm test

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable React components
│   │   ├── common/       # Common UI components
│   │   ├── layout/       # Layout components
│   │   ├── dashboard/    # Dashboard components
│   │   ├── products/     # Product components
│   │   ├── customers/    # Customer components
│   │   └── orders/       # Order components
│   ├── pages/            # Page components
│   ├── services/         # API services
│   ├── store/            # Redux store and slices
│   ├── hooks/            # Custom hooks
│   ├── types/            # TypeScript type definitions
│   ├── utils/            # Utility functions
│   ├── styles/           # Global styles
│   └── __tests__/        # Test files
├── public/               # Static assets
└── index.html            # HTML template
```

## Key Pages

- **Dashboard** - Real-time metrics and analytics
- **Products** - Product management and inventory
- **Customers** - Customer management and segmentation
- **Orders** - Order processing and tracking

## State Management

The app uses Redux Toolkit for global state management with the following slices:

- `auth` - Authentication state
- `products` - Product data and operations
- `customers` - Customer data and operations
- `orders` - Order data and operations

## API Integration

All API calls are centralized in `src/services/api.ts` using Axios. The service includes:

- Automatic token management
- Request/response interceptors
- Error handling
- Type-safe endpoints

## Testing

Tests are written using Vitest and React Testing Library. Run tests with:

```bash
npm test
```

Coverage report:

```bash
npm run test:coverage
```

Target: 95%+ coverage across all modules

## Linting and Formatting

```bash
# Lint code
npm run lint

# Format code
npm run format
```

## Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## License

MIT
