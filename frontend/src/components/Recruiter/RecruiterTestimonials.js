import React from 'react';
import Logo from '../HomePage/Logo';
import profile1 from '../../assets/linkedin-sample-1.jpeg';
import profile2 from '../../assets/linkedin-sample-2.jpeg';
import profile3 from '../../assets/linkedin-sample-3.jpeg';

const RecruiterTestimonials = () => {
    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl flex justify-center items-center font-semibold text-center text-teal-700 mb-8" style={{fontFamily: "Avenir"}}>
            Why our community loves OceaniaDevs
            <Logo />
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-lg shadow-lg flex flex-col justify-between bg-emerald-100">
              <p className="text-gray-800 mb-4 text-center" style={{fontFamily: "HeyWow"}}>
                "Other job boards feel like they're in the dinosaur age."
              </p>
              <div className="flex items-center justify-center mt-auto">
                <div className="w-12 h-12 bg-gray-300 rounded-full mr-4">
                  <img src={profile1} alt="Sarah Knox" className="rounded-full" />
                </div>
                <div style={{fontFamily: "Avenir"}}>
                  <p className="text-gray-900 font-bold">Sarah Knox</p>
                  <p className="text-gray-600">Hired at Flip Insurance</p>
                </div>
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-lg flex flex-col justify-between bg-orange-200">
              <p className="text-gray-800 mb-4 text-center" style={{fontFamily: "HeyWow"}}>
                "There are so many more interesting roles on Hatch compared to other job boards."
              </p>
              <div className="flex items-center justify-center mt-auto">
                <div className="w-12 h-12 bg-gray-300 rounded-full mr-4">
                  <img src={profile2}  alt="Thiago Meira" className="rounded-full" />
                </div>
                <div style={{fontFamily: "Avenir"}}>
                  <p className="text-gray-900 font-bold">Thiago Meira</p>
                  <p className="text-gray-600">Hired at Blend AI</p>
                </div>
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-lg flex flex-col justify-between bg-cyan-200">
              <p className="text-gray-800 mb-4 text-center" style={{fontFamily: "HeyWow"}}>
                "It makes a world of difference when there's more behind a job ad than just words on a page."
              </p>
              <div className="flex items-center justify-center mt-auto">
                <div className="w-12 h-12 bg-gray-300 rounded-full mr-4">
                  <img src={profile3}  alt="Piper Eddington" className="rounded-full" />
                </div>
                <div style={{fontFamily: "Avenir"}}>
                  <p className="text-gray-900 font-bold">Piper Eddington</p>
                  <p className="text-gray-600">Hired at Qantas</p>
                </div>
              </div>
            </div>
          </div>
        </div>
    )
}

export default RecruiterTestimonials;