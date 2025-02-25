import Layout from '@theme/Layout';
import React from 'react';

import Home from '../components/Home';

function HomePage() {
  return (
    <Layout
      title="ShortGPT: Automate Content Creation with AI"
      description="Automating video and short content creation with AI "
    >
      <Home />
    </Layout>
  );
}

export default HomePage;
