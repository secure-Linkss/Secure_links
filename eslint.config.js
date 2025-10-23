import js from '@eslint/js'
import react from 'eslint-plugin-react-hooks'

export default [
  js.configs.recommended,
  {
    plugins: { react },
    rules: {
      'no-unused-vars': 'warn',
      'no-console': 'warn'
    }
  }
]
