/**
 * Creating a sidebar enables you to:
 * - create an ordered group of docs
 * - render a sidebar for each doc of that group
 * - provide next/previous navigation.
 *
 * The sidebars can be generated from the filesystem, or explicitly defined here.
 *
 * Create as many sidebars as you want.
 */

module.exports = {
  docs: [
    {
      type: 'category',
      label: 'Introduction',
      collapsed: false,
      items: ['how-to-install', 'getting-started'],
    },
    {
      type: 'category',
      label: 'Content Engines',
      collapsed: false,
      items: ['content-video-engine', 'content-translation-engine', 'facts-short-engine'],
    },
    {
      type: 'category',
      label: 'API Key and Asset',
      collapsed: false,
      items: ['api-key-manager', 'asset-database'],
    },
  ],
};
