import React, { useState, useEffect } from 'react';
import { CheckCircle, X } from 'lucide-react';

const NotificationPopup = ({ message, actionText, actionHref, onDismiss }) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
      onDismiss();
    }, 7000);

    return () => clearTimeout(timer);
  }, [onDismiss]);

  if (!isVisible) return null;

  return (
    <div className="fixed top-4 right-4 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
      <div className="p-4">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <CheckCircle className="h-6 w-6 text-green-400" aria-hidden="true" />
          </div>
          <div className="ml-3 w-0 flex-1 pt-0.5">
            <p className="text-sm font-medium text-gray-900">Your profile has been updated!</p>
            <p className="mt-1 text-sm text-gray-500">{message}</p>
            <div className="mt-3 flex space-x-7">
              <button
                type="button"
                className="bg-white text-sm font-medium text-indigo-600 hover:text-indigo-500"
                onClick={() => {
                  setIsVisible(false);
                  onDismiss();
                }}
              >
                Dismiss
              </button>
              <a
                href={actionHref}
                className="bg-white text-sm font-medium text-indigo-600 hover:text-indigo-500"
              >
                {actionText}
              </a>
            </div>
          </div>
          <div className="ml-4 flex-shrink-0 flex">
            <button
              type="button"
              className="bg-white rounded-md inline-flex text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              onClick={() => {
                setIsVisible(false);
                onDismiss();
              }}
            >
              <span className="sr-only">Close</span>
              <X className="h-5 w-5" aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotificationPopup;