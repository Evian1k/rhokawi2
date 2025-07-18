import React from 'react';
import { cn } from '@/lib/utils';

const Sheet = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "fixed inset-0 z-50 flex",
      className
    )}
    {...props}
  />
));
Sheet.displayName = "Sheet";

const SheetTrigger = React.forwardRef(({ className, ...props }, ref) => (
  <button
    ref={ref}
    className={cn(className)}
    {...props}
  />
));
SheetTrigger.displayName = "SheetTrigger";

const SheetContent = React.forwardRef(({ 
  side = "right", 
  className, 
  children, 
  onClose,
  ...props 
}, ref) => (
  <div className="fixed inset-0 z-50">
    {/* Backdrop */}
    <div 
      className="fixed inset-0 bg-black/50 backdrop-blur-sm"
      onClick={onClose}
    />
    
    {/* Sheet Content */}
    <div
      ref={ref}
      className={cn(
        "fixed z-50 bg-background p-6 shadow-lg transition ease-in-out",
        "data-[state=open]:animate-in data-[state=closed]:animate-out",
        "data-[state=closed]:duration-300 data-[state=open]:duration-500",
        side === "right" && [
          "inset-y-0 right-0 h-full w-3/4 border-l",
          "data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right"
        ],
        side === "left" && [
          "inset-y-0 left-0 h-full w-3/4 border-r",
          "data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left"
        ],
        side === "top" && [
          "inset-x-0 top-0 border-b",
          "data-[state=closed]:slide-out-to-top data-[state=open]:slide-in-from-top"
        ],
        side === "bottom" && [
          "inset-x-0 bottom-0 border-t",
          "data-[state=closed]:slide-out-to-bottom data-[state=open]:slide-in-from-bottom"
        ],
        className
      )}
      {...props}
    >
      {children}
    </div>
  </div>
));
SheetContent.displayName = "SheetContent";

const SheetHeader = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "flex flex-col space-y-2 text-center sm:text-left",
      className
    )}
    {...props}
  />
));
SheetHeader.displayName = "SheetHeader";

const SheetTitle = React.forwardRef(({ className, ...props }, ref) => (
  <h2
    ref={ref}
    className={cn(
      "text-lg font-semibold text-foreground",
      className
    )}
    {...props}
  />
));
SheetTitle.displayName = "SheetTitle";

const SheetDescription = React.forwardRef(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
));
SheetDescription.displayName = "SheetDescription";

export {
  Sheet,
  SheetTrigger,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
};