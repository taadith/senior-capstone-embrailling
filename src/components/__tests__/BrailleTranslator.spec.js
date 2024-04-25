import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BrailleTranslator from '../BrailleTranslator.vue'

describe('BrailleTranslator.vue Test', () => {
    it('renders message when component is created', () => {
      // render the component
      const wrapper = mount(BrailleTranslator)
  
      // check that the title is rendered
      expect(wrapper.text()).toMatch('Help')
    })
  })