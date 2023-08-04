import { Hero } from '@algolia/ui-library';
import { useColorMode } from '@docusaurus/theme-common';
import { useBaseUrlUtils } from '@docusaurus/useBaseUrl';
import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  const { withBaseUrl } = useBaseUrlUtils();
  const { colorMode } = useColorMode();

  React.useEffect(() => {
    if (colorMode === 'dark') {
      document.querySelector('html').classList.add('dark');
    } else {
      document.querySelector('html').classList.remove('dark');
    }
  }, [colorMode]);

  function Header() {
    return (
      <Hero
        id="hero"
        title={
          <>

            <span className="hero-title text-4xl leading-10 font-extrabold text-blue-600 md:text-4xl lg:text-4xl md:leading-11 max-w-xs inline-block">
              🚀🎬 SHORTGPT
            </span>
            <span className="hero-title text-3xl leading-9 font-extrabold md:text-3xl lg:text-3xl md:leading-10 max-w-xxs inline-block">
              Opensource AI Content Automation Framework
            </span>
          </>
        }
        background="cubes"
        cta={[
          <Link
            key="get-started"
            to="/docs/how-to-install"
            className="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-semibold rounded-full text-white bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 hover:no-underline"
          >
            Get started
          </Link>
        ]}
      />
    );
  }

  function Description() {
    return (
      <>
        {/* Description */}
        <div className="py-8 overflow-hidden">
          <div className="relative max-w-xl mx-auto px-4 md:px-6 lg:px-8 lg:max-w-screen-xl">
            <div className="relative">
              <h3 className="text-center text-3xl leading-8 font-extrabold tracking-tight md:text-4xl md:leading-10">
                Automating video and short content creation with AI
              </h3>
              <p className="mt-4 max-w-3xl mx-auto text-center text-xl leading-7 text-description">
                ShortGPT is a powerful framework for automating content creation. It simplifies video creation, footage sourcing, voiceover synthesis, and editing tasks.
              </p>
            </div>

            <div className="pt-16">
              <ul className="lg:grid lg:grid-cols-3 lg:col-gap-8 lg:row-gap-10">
                <li>
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <div className="flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                        <svg
                          viewBox="0 0 20 20"
                          fill="currentColor"
                          className="search w-6 h-6"
                        >
                          <path
                            fillRule="evenodd"
                            d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                            clipRule="evenodd"
                          ></path>
                        </svg>
                      </div>
                    </div>
                    <div className="ml-4">
                      <h4 className="text-lg leading-6 font-medium">
                        Automated editing framework
                      </h4>
                      <p className="mt-2 text-base leading-6 text-description">
                        ShortGPT streamlines the video creation process with an LLM oriented video editing language, making it easier to automate editing tasks.
                      </p>
                    </div>
                  </div>
                </li>
                <li className="mt-10 lg:mt-0">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <div className="flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                        <svg
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          className="user-group w-6 h-6"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="2"
                            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                          ></path>
                        </svg>
                      </div>
                    </div>
                    <div className="ml-4">
                      <h4 className="text-lg leading-6 font-medium">
                        Voiceover / Content Creation
                      </h4>
                      <p className="mt-2 text-base leading-6 text-description">
                        ShortGPT supports multiple languages for voiceover synthesis, making it easy to create content in various languages.
                      </p>
                    </div>
                  </div>
                </li>
                <li className="mt-10 lg:mt-0">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <div className="flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                        <svg
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          className="device-mobile w-6 h-6"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="2"
                            d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"
                          ></path>
                        </svg>
                      </div>
                    </div>
                    <div className="ml-4">
                      <h4 className="text-lg leading-6 font-medium">
                        Asset Sourcing
                      </h4>
                      <p className="mt-2 text-base leading-6 text-description">
                        ShortGPT can source images and video footage from the internet, allowing you to easily find and use relevant visuals.
                      </p>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* How it works */}
        <div className="diagonal-box py-16 bg-gray-200 overflow-hidden">
          <div className="diagonal-content max-w-xl mx-auto px-4 md:px-6 lg:px-8 lg:max-w-screen-xl">
            <div className="max-w-screen-xl mx-auto pt-6 px-4 md:px-6 lg:px-8">
              <div className="max-w-4xl mx-auto text-center">
                <h2 className="text-3xl leading-9 font-extrabold text-gray-900 md:text-4xl md:leading-10">
                  How it works
                </h2>
                <p className="mt-4 max-w-2xl text-xl leading-7 text-gray-500 lg:mx-auto">
                ShortGPT is an AI-powered framework that automates the process of content creation, from script generation to asset sourcing and video editing.
                </p>
              </div>
            </div>

            <div className="py-16">
              <div className="max-w-xl mx-auto px-4 md:px-6 lg:max-w-screen-lg lg:px-8 ">
                <div className="lg:grid lg:grid-cols-3 lg:gap-8">
                  <div>
                    <div className="flex items-center justify-center">
                      <img
                        className="h-200"
                        src={withBaseUrl('img/assets/scraping.svg')}
                        width="190px"
                        height="220px"
                      />
                    </div>
                    <div className="mt-10 lg:mt-0 p-4">
                      <h5 className="text-lg leading-6 font-medium text-gray-900">
                        Automated Editing Framework
                      </h5>
                      <p className="mt-2 text-base leading-6 text-gray-600">
                      ShortGPT employs a heavy usage of LLMs and automated video editing libraries to streamline the video creation process (Ffmpeg, moviepy, ffprobe).
                      </p>
                    </div>
                  </div>
                  <div className="mt-10 lg:mt-0 p-4">
                    <div className="h-200 flex items-center justify-center">
                      <img
                        src={withBaseUrl('img/assets/configuration.svg')}
                        width="140px"
                        height="220px"
                        alt="Configuration of your crawler"
                      />
                    </div>
                    <div>
                      <h5 className="text-lg leading-6 font-medium text-gray-900">
                        Voiceover / Content Creation
                      </h5>
                      <p className="mt-2 text-base leading-6 text-gray-600">
                      ShortGPT integrates multiple neural voice synthesis engines (ElevenLabs, EdgeTTS), to allow human-like voice quality in the audio generated.
                      </p>
                    </div>
                  </div>
                  <div className="mt-10 lg:mt-0 p-4">
                    <div className="h-200 flex items-center justify-center">
                      <img
                        src={withBaseUrl('img/assets/implementation.svg')}
                        width="220px"
                        height="220px"
                        alt="Implementation on your website"
                      />
                    </div>
                    <div>
                      <h5 className="text-lg leading-6 font-medium text-gray-900">
                        Asset Sourcing
                      </h5>
                      <p className="mt-2 text-base leading-6 text-gray-600">
                      ShortGPT is equipped with an advanced asset sourcing module that can retrieve images and video footage from the internet. This feature allows for the easy incorporation of relevant visuals into the content (Pexels, youtube, and more soon).
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

    

        {/* Powered by AI */}
        <div className="py-16 bg-indigo-600 overflow-hidden lg:py-24">
          <div className="text-center">
            <h3 className="mt-2 text-3xl leading-8 font-extrabold text-white tracking-tight md:text-4xl md:leading-10">
              Powered by AI
            </h3>
          </div>
          <div className="relative max-w-xl mx-auto px-4 md:px-6 lg:px-8 lg:max-w-screen-xl">
            <div className="relative lg:grid lg:grid-cols-2 lg:gap-8 lg:items-center">
              <div className="relative">
                <ul className="mt-10">
                  <li className="mt-10">
                    <div className="flex">
                      <div className="flex-shrink-0">
                        <div className="flex items-center justify-center h-12 w-12 rounded-md bg-white text-indigo-500">
                          <svg
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            className="chip w-6 h-6"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth="2"
                              d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"
                            ></path>
                          </svg>
                        </div>
                      </div>
                      <div className="ml-4">
                        <h5 className="text-lg leading-6 font-medium text-white">
                          Automated Editing
                        </h5>
                        <p className="mt-2 text-base leading-6 text-gray-300">
                          ShortGPT automates the video editing process, making it faster and more efficient with the help of AI.
                        </p>
                      </div>
                    </div>
                  </li>
                  <li className="mt-10">
                    <div className="flex">
                      <div className="flex-shrink-0">
                        <div className="flex items-center justify-center h-12 w-12 rounded-md bg-white text-indigo-500">
                          <svg
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            className="chat w-6 h-6"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth="2"
                              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                            ></path>
                          </svg>
                        </div>
                      </div>
                      <div className="ml-4">
                        <h5 className="text-lg leading-6 font-medium text-white">
                          Voiceover / Content Creation
                        </h5>
                        <p className="mt-2 text-base leading-6 text-gray-300">
                          ShortGPT supports multiple languages for voiceover synthesis, making it easy to create content in various languages.
                        </p>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>

              <div className="relative">
                <ul className="mt-10">
                  <li className="mt-10">
                    <div className="flex">
                      <div className="flex-shrink-0">
                        <div className="flex items-center justify-center h-12 w-12 rounded-md bg-white text-indigo-500">
                          <svg
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            className="backspace w-6 h-6"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth="2"
                              d="M12 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2M3 12l6.414 6.414a2 2 0 001.414.586H19a2 2 0 002-2V7a2 2 0 00-2-2h-8.172a2 2 0 00-1.414.586L3 12z"
                            ></path>
                          </svg>
                        </div>
                      </div>
                      <div className="ml-4">
                        <h5 className="text-lg leading-6 font-medium text-white">
                          Asset Sourcing
                        </h5>
                        <p className="mt-2 text-base leading-6 text-gray-300">
                          ShortGPT can source images and video footage from the internet, allowing you to easily find and use relevant visuals.
                        </p>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </>
    )
  }



  return (
    <div id="tailwind">
      <Header />
      <Description />
    </div>
  );
}

export default Home;
