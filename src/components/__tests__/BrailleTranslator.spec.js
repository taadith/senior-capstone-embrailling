import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BrailleTranslator from '../../App.vue'

describe('BrailleTranslator.vue Test', () => {
    it('renders message when component is created', () => {
      // render the component
      const wrapper = mount(BrailleTranslator)
  
      // check that the text is rendered
      expect(wrapper.text()).toMatch('Translate PDF')
    })
    it('Test text disappears when button is pressed', async () => {
      // render the component
      const wrapper = mount(BrailleTranslator)
      const textBoxInput = wrapper.find('textarea')
      await textBoxInput.setValue("testing text!")
      await wrapper.get("button").trigger("click");
      expect(wrapper.text()).not.toMatch('testing text!')
  
      // check that the text is rendered
      expect(wrapper.text()).toMatch('Translate PDF')
    })
  })