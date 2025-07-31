# E-commerce Products Frontend

A React frontend application for displaying products using the FastAPI E-commerce Products API.

## 🚀 Features

- **Products List View**: Display all products in a responsive grid format
- **Product Detail View**: Show individual product details when clicked
- **API Integration**: Fetch data from your REST API endpoints
- **Search Functionality**: Search products by name, category, or brand
- **Pagination**: Navigate through large product lists
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: Handle loading states and error scenarios
- **Navigation**: Seamless navigation between list and detail views

## 🛠️ Technology Stack

- **React 18**: Modern React with hooks
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls
- **CSS3**: Custom styling with responsive design

## 📁 Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Header.js
│   │   ├── ProductCard.js
│   │   ├── ProductList.js
│   │   └── ProductDetail.js
│   ├── services/
│   │   └── api.js
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn
- FastAPI backend running on `http://localhost:8000`

### Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000`

## 🔧 Configuration

### API Configuration

The frontend is configured to connect to the FastAPI backend at `http://localhost:8000`. You can modify the API base URL in `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

### Proxy Configuration

The `package.json` includes a proxy configuration to avoid CORS issues during development:

```json
{
  "proxy": "http://localhost:8000"
}
```

## 📱 Features Overview

### 1. Products List View (`/`)

- **Grid Layout**: Responsive product grid with hover effects
- **Search Bar**: Search products by name, category, or brand
- **Pagination**: Navigate through pages of products
- **Product Cards**: Click to view detailed product information

### 2. Product Detail View (`/product/:id`)

- **Complete Product Info**: Display all product details
- **Back Navigation**: Return to products list
- **Error Handling**: Show appropriate messages for missing products
- **Responsive Layout**: Adapts to different screen sizes

### 3. Search Functionality

- **Real-time Search**: Search across product name, category, and brand
- **Search Results**: Display number of matching products
- **Clear Search**: Reset search and return to all products
- **Pagination**: Navigate through search results

### 4. Error Handling

- **Loading States**: Show loading indicators during API calls
- **Error Messages**: Display user-friendly error messages
- **Network Issues**: Handle API connection problems
- **404 Handling**: Handle missing products gracefully

## 🎨 Styling

The application uses custom CSS with:

- **Modern Design**: Clean, professional appearance
- **Responsive Grid**: Adapts to different screen sizes
- **Hover Effects**: Interactive product cards
- **Color Scheme**: Blue primary color with green accents
- **Typography**: System fonts for optimal readability

## 🔌 API Integration

The frontend integrates with the following API endpoints:

- `GET /api/products` - List all products with pagination
- `GET /api/products/{id}` - Get specific product by ID
- `GET /api/products/search` - Search products
- `GET /` - API information

## 🧪 Testing

To run tests:

```bash
npm test
```

## 📦 Build for Production

To create a production build:

```bash
npm run build
```

This creates a `build` folder with optimized files for deployment.

## 🚀 Deployment

The built application can be deployed to any static hosting service:

- **Netlify**: Drag and drop the `build` folder
- **Vercel**: Connect your GitHub repository
- **GitHub Pages**: Use the `build` folder
- **AWS S3**: Upload the `build` folder

## 🔧 Development

### Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App

### Code Structure

- **Components**: Reusable UI components
- **Services**: API integration layer
- **CSS**: Modular styling
- **Routing**: Client-side navigation

## 🎯 Key Features Implemented

✅ **Products List View**: Grid layout with pagination  
✅ **Product Detail View**: Complete product information  
✅ **API Integration**: Full integration with FastAPI backend  
✅ **Search Functionality**: Multi-field search with results  
✅ **Navigation**: Seamless routing between views  
✅ **Error Handling**: Comprehensive error management  
✅ **Loading States**: User feedback during API calls  
✅ **Responsive Design**: Mobile-friendly interface  
✅ **Modern UI**: Clean, professional styling  

## 🎉 Conclusion

This React frontend provides a complete user interface for the E-commerce Products API, featuring modern design, comprehensive functionality, and excellent user experience. The application is ready for production use and can be easily extended with additional features. 