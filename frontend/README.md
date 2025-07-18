# React Frontend

Modern React application for the Rhokawi Properties real estate platform, built with Vite, Tailwind CSS, and featuring a complete UI for property management.

## 🚀 Quick Start

### Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

## 🔧 Configuration

### Environment Variables (.env)
```env
VITE_API_URL=http://localhost:5000/api
```

## 🛠️ Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## 📁 Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/         # Page components
├── contexts/      # React contexts (Auth, Theme)
├── lib/          # Utilities and API client
└── main.jsx      # Application entry point
```

## 🎨 Technologies

- **React** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS
- **Radix UI** - Accessible UI components
- **Framer Motion** - Animation library
- **React Router** - Client-side routing

## 🔗 API Integration

The frontend is fully integrated with the Flask backend API through:
- `src/lib/api.js` - Complete API service layer
- JWT token management
- Role-based access control
- Real-time data fetching

## 📱 Features

- Responsive design for all devices
- Property search and filtering
- User authentication and profiles
- Property favorites system
- Contact form integration
- Admin/Agent/Client role management

## 🚀 Deployment

Deploy to Vercel, Netlify, or similar platforms:

1. Build the project: `npm run build`
2. Deploy the `dist` folder
3. Configure environment variables
4. Set up custom domain (optional)