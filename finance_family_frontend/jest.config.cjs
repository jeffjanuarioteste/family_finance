module.exports = {
  testEnvironment: 'jsdom',
  moduleFileExtensions: ['ts', 'js', 'vue', 'json'],
  moduleNameMapper: { '^@/(.*)$': '<rootDir>/src/$1' },
  transform: {
    '^.+\\.vue$': '@vue/vue3-jest',
    '^.+\\.ts$': ['ts-jest', { tsconfig: 'tsconfig.json', diagnostics: false }],
  },
  testMatch: ['<rootDir>/tests/**/*.spec.ts'],
}
