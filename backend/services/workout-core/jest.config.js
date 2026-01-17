export default {
  // Use the ESM preset for ts-jest
  preset: 'ts-jest/presets/default-esm', 
  testEnvironment: 'node',
  testMatch: ['**/*.test.ts'], 
  verbose: true,
  forceExit: true,
  moduleNameMapper: {
    // Allow imports with .js extensions to map to .ts files
    '^(\\.{1,2}/.*)\\.js$': '$1', 
  },
  transform: {
    // Configure ts-jest to process files with ESM support
    '^.+\\.tsx?$': [
      'ts-jest',
      {
        useESM: true,
      },
    ],
  },
};