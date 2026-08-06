'use client';

import { useState } from 'react';
import { Bars3Icon, BellIcon, UserCircleIcon } from '@heroicons/react/24/outline';
import { Menu, Transition } from '@headlessui/react';
import { Fragment } from 'react';

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-sm z-10">
      <div className="px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
        <button
          className="md:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
          onClick={() => setMobileMenuOpen(true)}
        >
          <Bars3Icon className="w-6 h-6" />
        </button>
        <div className="flex-1 flex items-center justify-end space-x-4">
          <button className="p-2 rounded-full text-gray-400 hover:text-gray-500 hover:bg-gray-100">
            <BellIcon className="w-6 h-6" />
          </button>
          <Menu as="div" className="relative">
            <Menu.Button className="flex items-center max-w-xs rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
              <UserCircleIcon className="w-8 h-8 text-gray-400" />
            </Menu.Button>
            <Transition
              as={Fragment}
              enter="transition ease-out duration-100"
              enterFrom="transform opacity-0 scale-95"
              enterTo="transform opacity-100 scale-100"
              leave="transition ease-in duration-75"
              leaveFrom="transform opacity-100 scale-100"
              leaveTo="transform opacity-0 scale-95"
            >
              <Menu.Items className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 ring-1 ring-black ring-opacity-5 focus:outline-none">
                <Menu.Item>
                  {({ active }) => (
                    <a
                      href="#"
                      className={`block px-4 py-2 text-sm ${
                        active ? 'bg-gray-100' : ''
                      }`}
                    >
                      Your Profile
                    </a>
                  )}
                </Menu.Item>
                <Menu.Item>
                  {({ active }) => (
                    <a
                      href="#"
                      className={`block px-4 py-2 text-sm ${
                        active ? 'bg-gray-100' : ''
                      }`}
                    >
                      Settings
                    </a>
                  )}
                </Menu.Item>
                <Menu.Item>
                  {({ active }) => (
                    <a
                      href="#"
                      className={`block px-4 py-2 text-sm ${
                        active ? 'bg-gray-100' : ''
                      }`}
                    >
                      Logout
                    </a>
                  )}
                </Menu.Item>
              </Menu.Items>
            </Transition>
          </Menu>
        </div>
      </div>
    </header>
  );
}