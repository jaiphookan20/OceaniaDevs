import React, { useState, useEffect } from 'react';
import { Link } from "react-router-dom";
import { ChevronDownIcon, BriefcaseIcon, CalendarIcon, CheckCircleIcon, XCircleIcon, ClockIcon, SearchIcon, FilterIcon, PlusIcon, ChevronLeft, ChevronRight } from 'lucide-react';
import { getRelativeTimeString } from '../../utils/time';
const applicationStatuses = [
  'All',
  'Applied',
  'Phone Screening',
  'Technical Interview',
  'Onsite Interview',
  'Offer Received',
  'Accepted',
  'Rejected',
  'Withdrawn'
];

const ITEMS_PER_PAGE = 10;

const ApplicationTrackingDashboard = () => {
  const [applications, setApplications] = useState([]);
  const [activeDropdown, setActiveDropdown] = useState(null);
  const [statusFilter, setStatusFilter] = useState('All');
  const [showFilterDropdown, setShowFilterDropdown] = useState(false);
  const [visibleItems, setVisibleItems] = useState(ITEMS_PER_PAGE);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      const response = await fetch('/api/user_applications', {
        method: 'GET',
        credentials: 'include'
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setApplications(data.applications);
      console.log(applications)
    } catch (error) {
      console.error('Error fetching applications:', error);
    }
  };

  const handleStatusChange = async (applicationId, newStatus) => {
    try {
      const response = await fetch(`/api/update_application_status/${applicationId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
        credentials: 'include'
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      setApplications(applications.map(app => 
        app.id === applicationId ? { ...app, status: newStatus } : app
      ));
      setActiveDropdown(null);
    } catch (error) {
      console.error('Error updating application status:', error);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Applied': return 'bg-lime-200 text-lime-700 border border-lime-300';
      case 'Phone Screening': return 'bg-violet-100 text-violet-800 border border-violet-300';
      case 'Technical Interview': return 'bg-teal-100 text-teal-800 border border-teal-300';
      case 'Onsite Interview': return 'bg-pink-100 text-pink-800 border border-pink-300';
      case 'Offer Received': return 'bg-yellow-100 text-yellow-800 border border-yellow-300';
      case 'Accepted': return 'bg-green-100 text-green-800 border border-green-300';
      case 'Rejected': return 'bg-red-100 text-red-800 border border-red-300';
      case 'Withdrawn': return 'bg-gray-100 text-gray-800 border  border-gray-300';
      default: return 'bg-blue-100 text-blue-300';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Applied': return <ClockIcon className="w-4 h-4" />;
      case 'Phone Screening': return <ClockIcon className="w-4 h-4" />;
      case 'Technical Interview': return <ClockIcon className="w-4 h-4" />;
      case 'Onsite Interview': return <ClockIcon className="w-4 h-4" />;
      case 'Offer Received': return <CheckCircleIcon className="w-4 h-4" />;
      case 'Accepted': return <CheckCircleIcon className="w-4 h-4" />;
      case 'Rejected': return <XCircleIcon className="w-4 h-4" />;
      case 'Withdrawn': return <XCircleIcon className="w-4 h-4" />;
      default: return <ClockIcon className="w-4 h-4" />;
    }
  };

  const filteredApplications = applications.filter(app => 
    (statusFilter === 'All' || app.status === statusFilter) &&
    app.company.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleViewMore = () => {
    setVisibleItems(prevVisibleItems => prevVisibleItems + ITEMS_PER_PAGE);
  };

  const clearFilter = () => {
    setStatusFilter('All');
  };

  const clearSearch = () => {
    setSearchTerm('');
  };

  return (
    <div className="min-h-screen bg-slate-50/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-10">
        <div className="bg-white overflow-hidden shadow-2xl">
          <div className="px-12 py-10 py-20 sm:p-6">
          <div className="flex justify-between">
            <nav className="flex items-center text-sm text-gray-500 mb-4 space-x-1">
              <Link to="/" className="hover:text-gray-700">OceaniaDevs</Link>
              <ChevronRight size={16} className="mx-2" />
              <Link to="/search-page" className="hover:text-gray-700">Search Jobs</Link>
              <ChevronRight size={16} className="mx-2" />
              <span className="text-gray-700">Application Dashboard</span>            
            </nav>
            <nav className="flex items-center text-sm text-gray-500 mb-4 space-x-1">
              <Link to="/applied-jobs" className="hover:text-gray-700">Applied Jobs</Link>
              <ChevronRight size={16} className="mx-2" />
            </nav>
          </div>
            <div className="sm:flex sm:items-center sm:justify-between border-t border-b border-slate-200 p-8">
              <div>
                <h1 className="text-6xl font-bold text-slate-600 sm:text-5xl bg-clip-text" style={{fontFamily:"Roobert-Regular, san-serif"}}>Application Dashboard</h1>
                <p className="mt-5 max-w-2xl text-lg text-slate-400" style={{fontFamily:"Avenir, san-serif"}}>Track and manage all your applications in one place</p>
              </div>
              {/* <img src={starLightLogo} className='h-24 w-24'/> */}
              {/* <div className="mt-4 sm:mt-0">
                <button className="inline-flex items-center px-4 py-2 border border-transparent rounded-full shadow-sm text-sm font-semibold text-white bg-black hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                  <PlusIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
                  Add New Application
                </button>
              </div> */}
            </div>

            <div className="mt-8 flex flex-col sm:flex-row sm:items-center sm:justify-between">
              <div className="flex-1 min-w-0">
                <div className="max-w-lg w-full lg:max-w-xs relative">
                  <label htmlFor="search" className="sr-only">Search</label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <SearchIcon className="h-5 w-5 text-gray-600" aria-hidden="true" />
                    </div>
                    <input
                      id="search"
                      name="search"
                      className="block w-full pl-10 pr-10 py-4 border border-gray-500 rounded-full leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-md"
                      placeholder="Search by company name"
                      type="search"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                    />
                    {searchTerm && (
                      <button
                        onClick={clearSearch}
                        className="absolute inset-y-0 right-0 pr-3 flex items-center"
                      >
                        <XCircleIcon className="h-5 w-5 text-gray-400 hover:text-gray-500" aria-hidden="true" />
                      </button>
                    )}
                  </div>
                </div>
              </div>
              <div className="mt-4 sm:mt-0 sm:ml-4 relative flex items-center">
                <button 
                  type="button" 
                  className="inline-flex items-center text-black text-lg bg-slate-600 font-medium px-4 py-2 border border-gray-300 rounded-full shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  onClick={() => setShowFilterDropdown(!showFilterDropdown)}
                  style={{fontFamily:"Avenir"}}
                >
                  <FilterIcon className="-ml-1 mr-2 h-5 w-5 text-gray-500" aria-hidden="true" />
                  Filter: {statusFilter}
                </button>
                {showFilterDropdown && (
                  <div className="absolute right-0 top-full z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                    <div className="py-1" role="menu" aria-orientation="vertical">
                      {applicationStatuses.map((status) => (
                        <button
                          key={status}
                          onClick={() => {
                            setStatusFilter(status);
                            setShowFilterDropdown(false);
                          }}
                          className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-lime-500 w-full text-left"
                          role="menuitem"
                        >
                          {status}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
                {statusFilter !== 'All' && (
                  <button
                    onClick={clearFilter}
                    className="ml-2 inline-flex items-center px-3 py-2 border border-gray-300 rounded-full text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    <XCircleIcon className="h-4 w-4 mr-1" />
                    Clear
                  </button>
                )}
              </div>
            </div>

            <div className="mt-8 flex flex-col">
              <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
                <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
                  <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-2xl mb-10">
                    <table className="min-w-full divide-y divide-gray-300">
                      <thead className="bg-violet-500" style={{fontFamily:"Avenir"}}>
                        <tr>
                          <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-md font-bold text-white sm:pl-6 w-1/4 text-center">Company</th>
                          <th scope="col" className="px-3 py-3.5 text-left text-md font-bold text-white w-1/3 text-center">Position</th>
                          <th scope="col" className="px-3 py-3.5 text-left text-md font-bold text-white w-1/6">Applied Date</th>
                          <th scope="col" className="px-3 py-3.5 text-left text-md font-bold text-white w-1/6">Status</th>
                          <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6 w-1/12">
                            <span className="sr-only">Actions</span>
                          </th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200 bg-white" style={{fontFamily:"Avenir"}}>
                            {filteredApplications.slice(0, visibleItems).map((application) => (
                          <tr key={application.id} className="hover:bg-gray-50 transition duration-150">
                            <td className="whitespace-wrap py-4 pl-4 pr-3 text-sm sm:pl-6 w-1/4">
                              <div className="flex items-center">
                                <div className="h-16 w-16 flex-shrink-0">
                                  <img className="h-16 w-16 rounded-full object-contain" src={application.logo} alt="" />
                                </div>
                                <div className="ml-8">
                                  <div className="font-semibold text-lg text-slate-800">{application.company}</div>
                                </div>
                              </div>
                            </td>
                            <td className="whitespace-normal px-3 py-4 text-md font-semibold text-slate-500 w-1/3">{application.position}</td>
                            <td className="whitespace-nowrap px-3 py-4 text-md text-gray-500 w-1/6">{getRelativeTimeString(application.appliedDate)}</td>
                            <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 w-1/6">
                              <span className={`inline-flex items-center px-4 py-2 rounded-full text-md font-medium ${getStatusColor(application.status)}`}>
                                {getStatusIcon(application.status)}
                                <span className="ml-1">{application.status}</span>
                              </span>
                            </td>
                            <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                              <div className="relative inline-block text-left">
                                <div>
                                  <button
                                    type="button"
                                    className="inline-flex items-center rounded-full border border-gray-300 bg-white px-3 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                                    id={`options-menu-${application.id}`}
                                    aria-haspopup="true"
                                    aria-expanded="true"
                                    onClick={() => setActiveDropdown(activeDropdown === application.id ? null : application.id)}
                                  >
                                    Update Status
                                    <ChevronDownIcon className="-mr-1 ml-2 h-5 w-5" aria-hidden="true" />
                                  </button>
                                </div>
                                {activeDropdown === application.id && (
                                  <div className="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none" 
                                       role="menu" 
                                       aria-orientation="vertical" 
                                       aria-labelledby={`options-menu-${application.id}`}
                                       style={{
                                         bottom: activeDropdown === application.id && filteredApplications.indexOf(application) >= filteredApplications.length - 3 ? '100%' : 'auto',
                                         top: activeDropdown === application.id && filteredApplications.indexOf(application) >= filteredApplications.length - 3 ? 'auto' : '100%'
                                       }}
                                  >
                                    <div className="py-1" role="none">
                                      {applicationStatuses.filter(status => status !== 'All').map((status) => (
                                        <button
                                          key={status}
                                          onClick={() => handleStatusChange(application.id, status)}
                                          className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-lime-500 w-full text-left"
                                          role="menuitem"
                                        >
                                          {status}
                                        </button>
                                      ))}
                                    </div>
                                  </div>
                                )}
                              </div>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
            {visibleItems < filteredApplications.length && (
              <div className="flex justify-center mt-4">
                <button
                  onClick={handleViewMore}
                  className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  View More
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ApplicationTrackingDashboard;