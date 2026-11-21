import { mount } from '@vue/test-utils'
import App from '@/app/App.vue'

describe('App', () => {
  it('renders title', () => {
    expect(mount(App).text()).toContain('Financeiro Familiar')
  })
})
